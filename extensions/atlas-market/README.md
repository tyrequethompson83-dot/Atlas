# ATLAS Market Read

This is an opt-in OpenClaw plugin for read-only data from a locally running MetaTrader 5 terminal. It adds three tools to OpenClaw's existing agent loop:

- atlas_market_quote
- atlas_market_candles
- atlas_market_structure

It is not enabled by this change. It does not read account balances or positions, place or modify orders, or make trading decisions.

## Windows prerequisites

1. Open the MT5 terminal you intend ATLAS to read. The adapter checks that a terminal process is already running and will not launch MT5 itself.
2. Set ATLAS_MT5_PYTHON in the environment available to the OpenClaw Gateway to the full path of the Python interpreter where the official MetaTrader5 package is installed. If it is already on PATH, the default is python.
3. If exactly one MT5 terminal is running, its path is used. If multiple terminals are running, set ATLAS_MT5_TERMINAL_PATH to the full path of the terminal executable that is already running.
4. Restart the Gateway after changing environment variables, then deliberately enable the plugin through OpenClaw's normal plugin configuration.

No API key is needed for this local read adapter. It does not retrieve account or position data. The exact symbol and, for candles/structure, timeframe must be supplied explicitly; the Forex Jarvis frontend's current-chart context has not been connected to OpenClaw yet.

## Local validation

Run the offline adapter tests from the repository root:

    python -m unittest discover -s extensions/atlas-market/bridge -p "test_*.py"

Then run the OpenClaw targeted checks for the extension in the source checkout. The offline tests do not validate a live terminal, Gateway tool selection, or model response.
