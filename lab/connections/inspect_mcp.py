import asyncio
import json
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_path = Path(__file__).resolve().with_name("mcp_server.py")
    server = StdioServerParameters(command=sys.executable, args=[str(server_path)])
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            listing = await session.list_tools()
            tools = [{"name": tool.name, "inputSchema": tool.inputSchema} for tool in listing.tools]
            print("tools/list")
            print(json.dumps(tools, ensure_ascii=False, indent=2))

            for name in ("read_input", "read_review_rules"):
                print(f"\ntools/call {name} {{}}")
                response = await session.call_tool(name, arguments={})
                if response.isError or not isinstance(response.structuredContent, dict):
                    raise SystemExit(f"{name} 실행에 실패했습니다.")
                print(json.dumps(response.structuredContent, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
