"""Narrow, read-only adapter from OpenClaw's ATLAS tools to local MetaTrader 5.

Only quote and OHLC retrieval are implemented. The adapter deliberately does
not expose order, account, position, history, or configuration operations.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
import math
import os
import re
import subprocess
import sys
from typing import Any

MAX_BARS = 200
DEFAULT_BARS = 100
SUPPORTED_TIMEFRAMES = {"M5", "M15", "M30", "H1", "H4"}
SYMBOL_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,31}$")
POWERSHELL_QUERY = (
    "$ErrorActionPreference = 'Stop'; "
    "Get-CimInstance Win32_Process "
    "-Filter \"Name = 'terminal64.exe' OR Name = 'terminal.exe'\" "
    "| Where-Object { $_.ExecutablePath } "
    "| Select-Object -ExpandProperty ExecutablePath"
)


def _value(record: Any, key: str, default: Any = None) -> Any:
    """Read both a mapping-like record and an MT5 numpy structured record."""
    try:
        return record[key]
    except (KeyError, TypeError, IndexError):
        return getattr(record, key, default)


def _finite_number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _utc_iso(timestamp: Any) -> str | None:
    number = _finite_number(timestamp)
    if number is None:
        return None
    try:
        return datetime.fromtimestamp(number, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    except (ValueError, OverflowError, OSError):
        return None


def validate_request(
    operation: str, symbol: str, timeframe: str | None = None, limit: str | int | None = None
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Return (validated request, error response); never accepts shell fragments."""
    if operation not in {"quote", "candles"}:
        return None, {"error": "Unsupported market operation."}
    if not isinstance(symbol, str) or not SYMBOL_PATTERN.fullmatch(symbol):
        return None, {"error": "Symbol is invalid. Use the exact broker symbol with letters, digits, dot, underscore, or hyphen only."}
    if operation == "quote":
        return {"operation": operation, "symbol": symbol}, None
    if not isinstance(timeframe, str) or timeframe.upper() not in SUPPORTED_TIMEFRAMES:
        return None, {"error": "Unsupported timeframe. Use M5, M15, M30, H1, or H4."}
    try:
        parsed_limit = DEFAULT_BARS if limit is None else int(limit)
    except (ValueError, TypeError, OverflowError):
        return None, {"error": "Candle limit must be an integer from 1 to 200."}
    if isinstance(limit, bool):
        return None, {"error": "Candle limit must be an integer from 1 to 200."}
    parsed_limit = max(1, min(MAX_BARS, parsed_limit))
    return {
        "operation": operation,
        "symbol": symbol,
        "timeframe": timeframe.upper(),
        "limit": parsed_limit,
    }, None


def build_quote_payload(
    symbol: str, tick: Any, symbol_info: Any, now: datetime | None = None
) -> dict[str, Any]:
    """Serialise a broker tick while preserving unknown timestamp/value fields."""
    retrieved = now or datetime.now(timezone.utc)
    if retrieved.tzinfo is None:
        retrieved = retrieved.replace(tzinfo=timezone.utc)
    timestamp = _utc_iso(_value(tick, "time"))
    age = None
    if timestamp:
        try:
            quoted = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            age = round(max(0.0, (retrieved - quoted).total_seconds()), 3)
        except (TypeError, ValueError, OverflowError):
            age = None

    digits_value = _finite_number(_value(symbol_info, "digits"))
    digits = int(digits_value) if digits_value is not None and 0 <= digits_value <= 10 else None
    bid_value = _finite_number(_value(tick, "bid"))
    ask_value = _finite_number(_value(tick, "ask"))
    result: dict[str, Any] = {
        "symbol": symbol,
        "source": "MetaTrader5.symbol_info_tick",
        "retrieved_at": retrieved.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "quote_time": timestamp,
        "age_seconds": age,
        "digits": digits,
    }
    if bid_value is not None:
        result["bid"] = round(bid_value, digits if digits is not None else 8)
    if ask_value is not None:
        result["ask"] = round(ask_value, digits if digits is not None else 8)
    if bid_value is not None and ask_value is not None:
        result["spread"] = round(ask_value - bid_value, digits if digits is not None else 8)
    if timestamp is None:
        result["warning"] = "The broker tick has no usable timestamp; freshness cannot be established."
    return result


def build_candles_payload(
    symbol: str,
    timeframe: str,
    rates: Any,
    limit: int,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Project MT5 rates to a bounded, timestamped OHLC shape."""
    retrieved = now or datetime.now(timezone.utc)
    if retrieved.tzinfo is None:
        retrieved = retrieved.replace(tzinfo=timezone.utc)
    rows: list[dict[str, Any]] = []
    for rate in list(rates or [])[-max(1, min(MAX_BARS, int(limit))):]:
        when = _utc_iso(_value(rate, "time"))
        open_value = _finite_number(_value(rate, "open"))
        high_value = _finite_number(_value(rate, "high"))
        low_value = _finite_number(_value(rate, "low"))
        close_value = _finite_number(_value(rate, "close"))
        volume_value = _finite_number(_value(rate, "tick_volume", _value(rate, "real_volume", 0)))
        if when is None or None in (open_value, high_value, low_value, close_value):
            continue
        rows.append({
            "time": when,
            "open": round(open_value, 8),
            "high": round(high_value, 8),
            "low": round(low_value, 8),
            "close": round(close_value, 8),
            "volume": int(max(0, volume_value or 0)),
        })
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "bars_returned": len(rows),
        "limit_applied": max(1, min(MAX_BARS, int(limit))),
        "oldest": rows[0]["time"] if rows else None,
        "newest": rows[-1]["time"] if rows else None,
        "source": "MetaTrader5.copy_rates_from_pos",
        "retrieved_at": retrieved.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "bars": rows,
    }


def _running_terminal_path() -> tuple[str | None, str | None]:
    """Find an already running terminal; fail closed rather than start one."""
    if os.name != "nt":
        return None, "This first adapter requires Windows and an already-running MetaTrader 5 terminal."
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", POWERSHELL_QUERY],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
    except (OSError, subprocess.SubprocessError):
        return None, "Could not verify that MetaTrader 5 is already running. The adapter will not launch it."
    paths = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    paths = [path for path in paths if os.path.basename(path).lower() in {"terminal64.exe", "terminal.exe"}]
    if result.returncode != 0 or not paths:
        return None, "MetaTrader 5 is not running. Start the terminal manually; this adapter will not launch it."

    configured = os.environ.get("ATLAS_MT5_TERMINAL_PATH", "").strip().strip('"')
    if configured:
        wanted = os.path.normcase(os.path.abspath(configured))
        matches = [path for path in paths if os.path.normcase(os.path.abspath(path)) == wanted]
        if len(matches) != 1:
            return None, "ATLAS_MT5_TERMINAL_PATH must identify a MetaTrader 5 terminal executable that is already running."
        return matches[0], None
    if len(paths) == 1:
        return paths[0], None
    return None, "Multiple MT5 terminals are running. Set ATLAS_MT5_TERMINAL_PATH to the full path of the terminal you want ATLAS to read."


def _read_from_mt5(request: dict[str, Any]) -> dict[str, Any]:
    terminal_path, terminal_error = _running_terminal_path()
    if terminal_error:
        return {"error": terminal_error}

    try:
        import MetaTrader5 as mt5
    except Exception:
        return {"error": "The selected Python interpreter cannot import the MetaTrader5 package. Set ATLAS_MT5_PYTHON to the interpreter used for the existing ATLAS MT5 installation."}

    initialized = False
    try:
        initialized = bool(mt5.initialize(path=terminal_path, timeout=5000))
        if not initialized:
            return {"error": "Could not connect to the already-running MT5 terminal. No market data was returned."}

        symbol = request["symbol"]
        info = mt5.symbol_info(symbol)
        if info is None:
            return {"error": f"MT5 does not expose the exact symbol {symbol!r}. No market data was returned."}

        if request["operation"] == "quote":
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                return {"error": f"MT5 has no tick for {symbol!r}. This is unavailable data, not a zero price."}
            return build_quote_payload(symbol, tick, info)

        timeframe = request["timeframe"]
        timeframe_code = getattr(mt5, "TIMEFRAME_" + timeframe, None)
        if not isinstance(timeframe_code, int):
            return {"error": f"The installed MT5 package does not expose timeframe {timeframe}."}
        rates = mt5.copy_rates_from_pos(symbol, timeframe_code, 0, request["limit"])
        if rates is None or len(rates) == 0:
            return {"error": f"MT5 returned no {timeframe} candles for {symbol!r}. The feed may be unavailable or history may not be loaded."}
        payload = build_candles_payload(symbol, timeframe, rates, request["limit"])
        if payload["bars_returned"] == 0:
            return {"error": f"MT5 returned no valid timestamped OHLC bars for {symbol!r} on {timeframe}."}
        return payload
    except Exception:
        return {"error": "The MT5 read failed. No market data was returned."}
    finally:
        if initialized:
            try:
                mt5.shutdown()
            except Exception:
                pass


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    operation = args[0] if len(args) > 0 else ""
    symbol = args[1] if len(args) > 1 else ""
    timeframe = args[2] if len(args) > 2 else None
    limit = args[3] if len(args) > 3 else None
    request, error = validate_request(operation, symbol, timeframe, limit)
    payload = error if error else _read_from_mt5(request or {})
    print(json.dumps(payload, ensure_ascii=True, separators=(",", ":"), allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
