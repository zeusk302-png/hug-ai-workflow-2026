from typing import Literal

from mcp.server.fastmcp import FastMCP

server = FastMCP("HUG card styles")


@server.tool()
def get_card_style(audience: Literal["children", "exhibit"]) -> dict[str, str]:
    """Return the writing rules for a classroom photo card."""
    rules = {
        "children": "Use simple words and write two short sentences.",
        "exhibit": "Write two sentences with context and retain the source.",
    }
    return {"audience": audience, "rule": rules[audience]}


if __name__ == "__main__":
    server.run(transport="stdio")
