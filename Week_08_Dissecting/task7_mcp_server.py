"""Task 7: a local MCP server with one tool, exchange_rate.

Uses the official MCP Python SDK (mcp 2.x) and the free Frankfurter API
(https://frankfurter.dev, European Central Bank rates, no API key).
Claude Code starts it over stdio, see .mcp.json in the repository root.
"""

import json
import urllib.error
import urllib.request

from mcp.server import MCPServer

server = MCPServer("exchange-rate")


@server.tool()
def exchange_rate(from_currency: str, to_currency: str, amount: float = 1.0) -> str:
    """Convert an amount between two currencies using today's ECB rate.

    Currencies are three-letter codes such as EUR, CZK, USD or GBP.
    """
    base = from_currency.strip().upper()
    target = to_currency.strip().upper()
    url = f"https://api.frankfurter.dev/v1/latest?base={base}&symbols={target}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        return f"Unknown currency code or bad request ({error.code}): {base} -> {target}"
    except urllib.error.URLError as error:
        return f"Could not reach the exchange rate service: {error.reason}"

    rate = data["rates"][target]
    return f"{amount:g} {base} = {amount * rate:.2f} {target} (rate {rate}, ECB data from {data['date']})"


if __name__ == "__main__":
    server.run()
