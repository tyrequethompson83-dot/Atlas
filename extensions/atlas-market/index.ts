import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import { Type } from "typebox";
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

const execFileAsync = promisify(execFile);
const bridgePath = fileURLToPath(new URL("./bridge/mt5_read.py", import.meta.url));
const SYMBOL_PATTERN = "^[A-Za-z0-9][A-Za-z0-9._-]{0,31}$";
const TIMEFRAMES = ["M5", "M15", "M30", "H1", "H4"] as const;
const MAX_BARS = 200;
const DEFAULT_BARS = 100;
const RUN_TIMEOUT_MS = 15_000;
const MAX_BUFFER_BYTES = 1_048_576;

type JsonRecord = Record<string, unknown>;
type BridgeResult = JsonRecord & { error?: string };

const childEnvironmentKeys = [
  "PATH",
  "SystemRoot",
  "WINDIR",
  "TEMP",
  "TMP",
  "USERPROFILE",
  "LOCALAPPDATA",
  "APPDATA",
  "PROGRAMFILES",
  "PYTHONHOME",
  "PYTHONPATH",
  "VIRTUAL_ENV",
  "ATLAS_MT5_TERMINAL_PATH",
  "PYTHONUTF8",
] as const;

function safeChildEnvironment(): NodeJS.ProcessEnv {
  const result: NodeJS.ProcessEnv = {};
  for (const key of childEnvironmentKeys) {
    const value = process.env[key];
    if (value !== undefined) result[key] = value;
  }
  result.PYTHONUTF8 = "1";
  return result;
}

function parseJson(stdout: string | undefined): BridgeResult | undefined {
  if (!stdout) return undefined;
  try {
    const parsed: unknown = JSON.parse(stdout);
    if (parsed !== null && typeof parsed === "object" && !Array.isArray(parsed)) {
      return parsed as BridgeResult;
    }
  } catch {
    // Invalid subprocess output is an unavailable source, never market data.
  }
  return undefined;
}

async function runBridge(argv: string[]): Promise<BridgeResult> {
  const python = process.env.ATLAS_MT5_PYTHON?.trim() ||
    (process.platform === "win32" ? "python" : "python3");
  try {
    const { stdout } = await execFileAsync(python, [bridgePath, ...argv], {
      timeout: RUN_TIMEOUT_MS,
      maxBuffer: MAX_BUFFER_BYTES,
      windowsHide: true,
      env: safeChildEnvironment(),
    });
    const result = parseJson(stdout);
    return result ?? { error: "The local MT5 adapter returned invalid data; no market value is available." };
  } catch (error) {
    const result = parseJson((error as { stdout?: string }).stdout);
    if (result) return result;
    const code = (error as { code?: string }).code;
    if (code === "ENOENT") {
      return {
        error: "Python could not be started. Set ATLAS_MT5_PYTHON to the full path of the Python interpreter that has the MetaTrader5 package installed.",
      };
    }
    if ((error as { killed?: boolean }).killed) {
      return { error: "The local MT5 read timed out; no market value is available." };
    }
    return { error: "The local MT5 read adapter failed; no market value is available." };
  }
}

function toolResult(data: BridgeResult): {
  content: { type: "text"; text: string }[];
  details: BridgeResult;
} {
  return {
    content: [{
      type: "text",
      text: typeof data.error === "string"
        ? "Market data unavailable: " + data.error
        : JSON.stringify(data, null, 2),
    }],
    details: data,
  };
}

type Bar = {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
};

function structureFromBars(bars: Bar[]): JsonRecord {
  const radius = 2;
  const swingHighs: { time: string; price: number }[] = [];
  const swingLows: { time: string; price: number }[] = [];

  for (let i = radius; i < bars.length - radius; i += 1) {
    const bar = bars[i];
    const neighbors = [
      ...bars.slice(i - radius, i),
      ...bars.slice(i + 1, i + radius + 1),
    ];
    if (neighbors.every((other) => bar.high > other.high)) {
      swingHighs.push({ time: bar.time, price: bar.high });
    }
    if (neighbors.every((other) => bar.low < other.low)) {
      swingLows.push({ time: bar.time, price: bar.low });
    }
  }

  const windowHigh = bars.length ? Math.max(...bars.map((bar) => bar.high)) : null;
  const windowLow = bars.length ? Math.min(...bars.map((bar) => bar.low)) : null;
  const lastClose = bars.length ? bars[bars.length - 1].close : null;
  const span = windowHigh !== null && windowLow !== null ? windowHigh - windowLow : 0;
  const rangePosition = lastClose !== null && windowLow !== null && span > 0
    ? Number(((lastClose - windowLow) / span).toFixed(4))
    : null;

  return {
    swing_highs: swingHighs.slice(-6),
    swing_lows: swingLows.slice(-6),
    window_high: windowHigh,
    window_low: windowLow,
    last_close: lastClose,
    range_position: rangePosition,
    swing_confirmation_radius: radius,
    note: "Descriptive structure calculated from these returned bars, not from an indicator or chart overlay. Range position is 0 at the window low and 1 at the high.",
  };
}

function validBars(data: BridgeResult): Bar[] | undefined {
  if (!Array.isArray(data.bars)) return undefined;
  const bars = data.bars as unknown[];
  if (!bars.every((bar) => {
    if (!bar || typeof bar !== "object") return false;
    const row = bar as Record<string, unknown>;
    return typeof row.time === "string" &&
      ["open", "high", "low", "close", "volume"].every((key) => typeof row[key] === "number" && Number.isFinite(row[key]));
  })) return undefined;
  return bars as Bar[];
}

const symbolSchema = Type.String({
  minLength: 1,
  maxLength: 32,
  pattern: SYMBOL_PATTERN,
  description: "Exact broker symbol, e.g. XAUUSDm. Must match a symbol exposed by the running MT5 terminal.",
});
const timeframeSchema = Type.Union(TIMEFRAMES.map((timeframe) => Type.Literal(timeframe)));
const limitSchema = Type.Optional(Type.Integer({
  minimum: 1,
  maximum: MAX_BARS,
  description: "Maximum number of most recent candles. Hard-capped at 200.",
}));

export default definePluginEntry({
  id: "atlas-market",
  name: "ATLAS Market Read",
  description: "Read-only MT5 quote, OHLC, and descriptive market-structure tools.",
  register(api) {
    api.registerTool({
      name: "atlas_market_quote",
      description: "Read the bid, ask, spread, broker quote timestamp/age, and symbol precision for one explicitly named MT5 symbol. Read-only; does not read account or position data.",
      parameters: Type.Object({
        symbol: symbolSchema,
      }, { additionalProperties: false }),
      async execute(_toolCallId, params) {
        const result = await runBridge(["quote", params.symbol]);
        return toolResult(result);
      },
    });

    api.registerTool({
      name: "atlas_market_candles",
      description: "Read a bounded series of MT5 OHLC candles for an explicitly named symbol and timeframe. Use exact timestamps and the source metadata; missing feed data must remain unknown, not zero.",
      parameters: Type.Object({
        symbol: symbolSchema,
        timeframe: timeframeSchema,
        limit: limitSchema,
      }, { additionalProperties: false }),
      async execute(_toolCallId, params) {
        const limit = typeof params.limit === "number" ? params.limit : DEFAULT_BARS;
        const result = await runBridge([
          "candles",
          params.symbol,
          params.timeframe,
          String(Math.max(1, Math.min(MAX_BARS, limit))),
        ]);
        return toolResult(result);
      },
    });

    api.registerTool({
      name: "atlas_market_structure",
      description: "Read bounded MT5 candles and calculate descriptive two-bar fractal swing highs/lows plus close position in the observed range. Requires explicit symbol and timeframe. This is not an indicator, forecast, or trade signal.",
      parameters: Type.Object({
        symbol: symbolSchema,
        timeframe: timeframeSchema,
        limit: limitSchema,
      }, { additionalProperties: false }),
      async execute(_toolCallId, params) {
        const limit = typeof params.limit === "number" ? params.limit : DEFAULT_BARS;
        const data = await runBridge([
          "candles",
          params.symbol,
          params.timeframe,
          String(Math.max(1, Math.min(MAX_BARS, limit))),
        ]);
        if (typeof data.error === "string") return toolResult(data);
        const bars = validBars(data);
        if (!bars || bars.length === 0) {
          return toolResult({ error: "MT5 returned no valid candles, so structure cannot be calculated." });
        }
        return toolResult({
          ...data,
          structure: structureFromBars(bars),
        });
      },
    });
  },
});
