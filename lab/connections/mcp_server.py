from mcp.server.fastmcp import FastMCP

from input_source import read_input as read_lesson_input


server = FastMCP("HUG connection lab")


@server.tool()
def read_input() -> dict[str, str | None]:
    """Read the exercise's input.txt and return its status and UTF-8 text."""
    return read_lesson_input()


if __name__ == "__main__":
    # Standard streams carry MCP messages to and from the inspector.
    server.run(transport="stdio")
