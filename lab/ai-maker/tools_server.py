"""Read-only tools for the fictional newsletter archive."""
import argparse
import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

SAMPLES = Path(__file__).with_name("samples.json")
server = FastMCP("Personal collection")
trace_path: Path | None = None


def record(tool: str, arguments: dict, returned: dict) -> dict:
    if trace_path:
        # stdout belongs to the MCP protocol. The launcher gets a separate trace.
        event = {"tool": tool, "arguments": arguments, "returned": returned}
        with trace_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, ensure_ascii=False) + "\n")
    return returned


@server.tool()
def find_sources(keyword: str = "") -> dict[str, list[dict[str, str]]]:
    """List matching titles and IDs for both issues. Empty keyword lists all. Use a short Korean keyword."""
    keyword = keyword.strip().casefold()
    items = []
    for source in json.loads(SAMPLES.read_text(encoding="utf-8")):
        if keyword in " ".join(source.values()).casefold():
            items.append({field: source[field] for field in ("id", "title", "period", "channel")})
    return record("find_sources", {"keyword": keyword}, {"items": items})


@server.tool()
def read_source(source_id: str) -> dict[str, dict[str, str] | str]:
    """Read one full source by its exact ID from find_sources, including text to cite."""
    for source in json.loads(SAMPLES.read_text(encoding="utf-8")):
        if source["id"] == source_id:
            return record("read_source", {"source_id": source_id}, {"source": source})
    return record("read_source", {"source_id": source_id}, {"message": "그 ID의 자료가 없습니다."})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", type=Path)
    trace_path = parser.parse_args().trace
    server.run(transport="stdio")
