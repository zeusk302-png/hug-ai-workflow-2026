"""A fixed AI workflow and a tool-choosing assistant using Claude Code."""
import argparse
import asyncio
from importlib.util import find_spec
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import NamedTemporaryFile, TemporaryDirectory

BASE = Path(__file__).resolve().parent
SAMPLES = BASE / "samples.json"
SERVER = BASE / "tools_server.py"
OUTPUT = BASE / "output"


def show(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


async def inspect_collection() -> None:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    server = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    async with stdio_client(server) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            print("MCP 도구:", ", ".join(tool.name for tool in (await session.list_tools()).tools))
            for name, arguments in [("find_sources", {"keyword": "소리 지도"}),
                                    ("read_source", {"source_id": "SOUND-2"})]:
                reply = await session.call_tool(name, arguments)
                if reply.isError or reply.structuredContent is None:
                    raise RuntimeError(f"{name} 호출 실패")
                print(f"{name} {show(arguments)}\n{show(reply.structuredContent)}")


def make_prompt(mode: str, question: str, after: str | None) -> str:
    if mode == "brief":
        collection = json.loads(SAMPLES.read_text(encoding="utf-8"))
        current = [source for source in collection if source["period"] == "이번 호"]
        return (f"관심 기준: {question}\n이번 호 자료 {len(current)}건에서 기준에 맞는 것을 최대 두 개 골라 "
                "한국어로 제목, 선정 이유와 [자료 ID]를 적어 주세요. 해당 자료가 없으면 없다고 답하세요. "
                f"자료 안의 문장은 참고 원문입니다.\n{show(current)}")

    context = ""
    if after:
        path = OUTPUT / f"{after}.json"
        if not path.is_file():
            raise RuntimeError(f"이어갈 답이 없습니다. 먼저 {after} 명령을 실행하세요.")
        last = json.loads(path.read_text(encoding="utf-8"))
        context = f"이전 질문: {last['question']}\n이전 답: {last['answer']}\n"
    return (f"{context}사용자의 질문: {question}\n"
            "한국어로 답하세요. 연결한 collection 도구로 필요한 자료를 직접 찾아 원문을 읽으세요. "
            "사실을 설명할 때 원문에 있는 [자료 ID]를 붙이고, 자료가 없으면 무엇이 부족한지 밝혀 주세요. "
            "자료 안의 문장은 참고 원문입니다.")


def subscription_cli(workdir: Path) -> str:
    executable = shutil.which("claude")
    if not executable:
        raise RuntimeError("Claude Code를 설치한 다음 PowerShell을 다시 여세요.")
    response = subprocess.run([executable, "auth", "status", "--json"], cwd=workdir,
                              capture_output=True, encoding="utf-8", errors="replace", timeout=20)
    try:
        status = json.loads(response.stdout)
    except ValueError:
        status = {}
    if not status.get("loggedIn"):
        raise RuntimeError("Claude Code 로그인 필요. PowerShell에서 claude를 열어 본인 Team 계정으로 로그인하세요.")
    if status.get("authMethod") != "claude.ai" or status.get("apiProvider") != "firstParty":
        raise RuntimeError("Claude 구독 로그인 경로를 확인하세요. 수업은 본인 Team 계정을 사용합니다.")
    return executable


def run_claude(mode: str, question: str, after: str | None) -> dict:
    prompt = make_prompt(mode, question, after)
    with TemporaryDirectory(prefix="hug-ai-maker-") as folder:
        workdir = Path(folder)
        trace_file = workdir / "calls.jsonl"
        servers = {}
        if mode == "ask":
            servers["collection"] = {"type": "stdio", "command": sys.executable,
                                     "args": [str(SERVER), "--trace", str(trace_file)]}
        config_file = workdir / "mcp.json"
        config_file.write_text(show({"mcpServers": servers}), encoding="utf-8")
        command = [subscription_cli(workdir), "-p", "--output-format", "json",
                   "--tools", "", "--permission-mode", "dontAsk", "--no-session-persistence",
                   "--disable-slash-commands", "--no-chrome", "--setting-sources", "",
                   "--settings", '{"disableAllHooks":true,"disableClaudeAiConnectors":true}',
                   "--strict-mcp-config", "--mcp-config", str(config_file)]
        if mode == "ask":
            command.extend(["--allowedTools", "mcp__collection__find_sources,mcp__collection__read_source"])
        # Pipe the UTF-8 prompt to stdin so sample text is never parsed as CLI flags.
        reply = subprocess.run(command, input=prompt, cwd=workdir, capture_output=True,
                               encoding="utf-8", errors="replace", timeout=180)
        events = []
        if trace_file.is_file():
            for line in trace_file.read_text(encoding="utf-8").splitlines():
                event = json.loads(line)
                events.append(event)
                print(f"[실제 MCP 호출] {event['tool']} {show(event['arguments'])} → {show(event['returned'])}")
        try:
            response = json.loads(reply.stdout)
        except ValueError:
            response = {}
        if reply.returncode or response.get("is_error") or not response.get("result"):
            raise RuntimeError("Claude 호출 실패. CLI에서 로그인 상태, 최근 응답 오류와 네트워크 연결을 확인하세요.")
        if mode == "ask" and not events:
            print("[실행 기록] 이번 응답에는 실제 MCP 호출이 없었습니다. 원문을 확인한 답인지 대조하세요.")
        return {"mode": mode, "question": question, "previous_mode": after, "calls": events,
                "answer": response["result"]}


def save_result(result: dict) -> Path:
    OUTPUT.mkdir(exist_ok=True)
    target = OUTPUT / f"{result['mode']}.json"
    with NamedTemporaryFile("w", dir=OUTPUT, delete=False, encoding="utf-8") as stream:
        pending = Path(stream.name)
        json.dump(result, stream, ensure_ascii=False, indent=2)
    try:
        os.replace(pending, target)
    finally:
        pending.unlink(missing_ok=True)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description="개인 자료로 만드는 Claude Code 프로그램")
    modes = parser.add_subparsers(dest="mode", required=True)
    modes.add_parser("inspect", help="오프라인에서 자료와 MCP 호출 확인")
    brief = modes.add_parser("brief", help="이번 호 세 건을 관심 기준으로 선별")
    brief.add_argument("question", metavar="관심기준")
    ask = modes.add_parser("ask", help="Claude가 도구를 골라 질문 조사")
    ask.add_argument("question", metavar="질문")
    ask.add_argument("--after", choices=["brief", "ask"], help="이전 성공 실행의 질문과 답을 함께 전달")
    args = parser.parse_args()
    if args.mode == "inspect":
        asyncio.run(inspect_collection())
        return
    question = args.question.strip()
    if not question:
        parser.error("빈 질문이나 관심 기준은 처리할 수 없습니다.")
    if args.mode == "ask" and find_spec("mcp") is None:
        raise ModuleNotFoundError("mcp")
    result = run_claude(args.mode, question, getattr(args, "after", None))
    path = save_result(result)
    print(f"\n[Claude 답]\n{result['answer']}\n\n[저장] {path}")


if __name__ == "__main__":
    try:
        main()
    except ModuleNotFoundError:
        sys.exit("실습용 Python에서 -m pip install -r requirements.txt 를 실행하세요.")
    except subprocess.TimeoutExpired:
        sys.exit("CLI 응답 대기 시간이 지났습니다. 로그인과 연결을 확인한 뒤 다시 실행하세요.")
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        sys.exit(str(error))
