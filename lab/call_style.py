import argparse
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def get_style(audience: str, *, show_schema: bool = False) -> dict:
    server_path = Path(__file__).with_name("style_server.py")
    server = StdioServerParameters(command=sys.executable, args=[str(server_path)])
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            if show_schema:
                result = await session.list_tools()
                print("MCP tools/list")
                for tool in result.tools:
                    print(json.dumps({"name": tool.name, "inputSchema": tool.inputSchema}, indent=2))
            arguments = {"audience": audience}
            if show_schema:
                print(f"\nMCP tools/call get_card_style {json.dumps(arguments)}")
            response = await session.call_tool("get_card_style", arguments)
            if response.isError or not isinstance(response.structuredContent, dict):
                raise RuntimeError(f"Tool failed: {response.content}")
            return response.structuredContent


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audience", nargs="?", choices=("children", "exhibit"), default="children")
    style = asyncio.run(get_style(parser.parse_args().audience, show_schema=True))
    print(json.dumps(style, indent=2, ensure_ascii=False))
