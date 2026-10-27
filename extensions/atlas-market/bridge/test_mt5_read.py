"""Offline unit tests for the safe input and data-projection parts of the MT5 bridge."""

from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).with_name("mt5_read.py")
SPEC = importlib.util.spec_from_file_location("atlas_mt5_read", MODULE_PATH)
assert SPEC and SPEC.loader
mt5_read = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mt5_read)


class ValidateRequestTests(unittest.TestCase):
    def test_quote_accepts_exact_broker_symbol(self):
        request, error = mt5_read.validate_request("quote", "XAUUSDm")
        self.assertIsNone(error)
        self.assertEqual(request, {"operation": "quote", "symbol": "XAUUSDm"})

    def test_shell_metacharacters_are_rejected(self):
        request, error = mt5_read.validate_request("quote", "XAUUSDm;whoami")
        self.assertIsNone(request)
        self.assertIn("invalid", error["error"].lower())

    def test_only_supported_timeframes_are_accepted(self):
        request, error = mt5_read.validate_request("candles", "XAUUSDm", "M15", "40")
        self.assertIsNone(error)
        self.assertEqual(request["limit"], 40)
        request, error = mt5_read.validate_request("candles", "XAUUSDm", "D1", "40")
        self.assertIsNone(request)
        self.assertIn("Unsupported timeframe", error["error"])

    def test_candle_count_is_hard_bounded(self):
        request, error = mt5_read.validate_request("candles", "XAUUSDm", "M15", "99999")
        self.assertIsNone(error)
        self.assertEqual(request["limit"], mt5_read.MAX_BARS)

    def test_unsupported_operation_fails_closed(self):
        request, error = mt5_read.validate_request("order_send", "XAUUSDm")
        self.assertIsNone(request)
        self.assertEqual(error, {"error": "Unsupported market operation."})


class ProjectionTests(unittest.TestCase):
    def test_quote_preserves_timestamp_and_does_not_invent_values(self):
        now = datetime(2026, 10, 27, 12, 0, tzinfo=timezone.utc)
        tick = {"time": 1793102340, "bid": 4000.12, "ask": 4000.22}
        info = {"digits": 2}
        result = mt5_read.build_quote_payload("XAUUSDm", tick, info, now=now)
        self.assertEqual(result["bid"], 4000.12)
        self.assertEqual(result["ask"], 4000.22)
        self.assertIsNotNone(result["quote_time"])
        self.assertIn("age_seconds", result)
        self.assertNotIn("balance", result)
        self.assertNotIn("positions", result)

    def test_quote_missing_timestamp_stays_unknown(self):
        now = datetime(2026, 10, 27, 12, 0, tzinfo=timezone.utc)
        result = mt5_read.build_quote_payload("XAUUSDm", {"bid": 10, "ask": 11}, {"digits": 2}, now=now)
        self.assertIsNone(result["quote_time"])
        self.assertIsNone(result["age_seconds"])
        self.assertIn("warning", result)

    def test_candle_projection_is_bounded_timestamped_and_compact(self):
        now = datetime(2026, 10, 27, 12, 0, tzinfo=timezone.utc)
        rates = [
            {"time": 1793100000 + i * 900, "open": 2000 + i, "high": 2002 + i,
             "low": 1999 + i, "close": 2001 + i, "tick_volume": 100 + i}
            for i in range(5)
        ]
        result = mt5_read.build_candles_payload("XAUUSDm", "M15", rates, 3, now=now)
        self.assertEqual(result["bars_returned"], 3)
        self.assertEqual(len(result["bars"]), 3)
        self.assertLessEqual(result["bars_returned"], result["limit_applied"])
        self.assertTrue(result["bars"][0]["time"].endswith("Z"))
        self.assertIn("retrieved_at", result)
        self.assertNotIn("account", result)
        self.assertNotIn("positions", result)


if __name__ == "__main__":
    unittest.main()
