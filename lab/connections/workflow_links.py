import asyncio
from datetime import timedelta
from pathlib import Path
import sys

from local_http import CPU_PATH, CPU_PORT, INPUT_PATH, INPUT_PORT, request_json


class WorkflowLinkError(Exception):
    pass


def need_text(result: dict, source: str) -> str:
    status = result.get("status")
    text = result.get("text")
    if status != "ok" or not isinstance(text, str) or not text.strip():
        raise WorkflowLinkError(f"{source}에서 읽을 수 있는 텍스트가 없습니다. 상태 · {status}")
    return text


def read_api_input() -> str:
    result = request_json("GET", INPUT_PORT, INPUT_PATH)
    return need_text(result, "입력 API")


async def _call_tool(mcp_server_path: Path, name: str, arguments: dict) -> dict:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(mcp_server_path.resolve())],
    )
    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=15)) as session:
            await session.initialize()
            result = await session.call_tool(name, arguments=arguments)
            if result.isError or not isinstance(result.structuredContent, dict):
                raise WorkflowLinkError(f"MCP의 {name} 결과를 읽지 못했습니다.")
            return result.structuredContent


def _request_mcp_tool(mcp_server_path: Path, name: str, arguments: dict) -> dict:
    if not mcp_server_path.is_file():
        raise WorkflowLinkError("MCP 서버 파일의 경로를 확인하세요.")
    try:
        return asyncio.run(_call_tool(mcp_server_path, name, arguments))
    except ModuleNotFoundError as error:
        raise WorkflowLinkError("실습 폴더의 .venv Python으로 실행하세요.") from error
    except Exception as error:
        raise WorkflowLinkError(f"MCP 도구 {name} 호출에 실패했습니다. 서버 경로와 실습 환경을 확인하세요.") from error


def read_mcp_rules(mcp_server_path: Path) -> str:
    result = _request_mcp_tool(mcp_server_path, "read_review_rules", {})
    return need_text(result, "검토 기준 MCP")


def search_mcp_evidence(mcp_server_path: Path, query: str) -> list[dict]:
    result = _request_mcp_tool(mcp_server_path, "search_evidence", {"query": query})
    evidence = result.get("evidence")
    if not isinstance(evidence, list):
        raise WorkflowLinkError("MCP 응답에 검색 결과 목록이 없습니다.")
    if not evidence:
        raise WorkflowLinkError("검색 결과 0건. 모델을 호출하지 않았습니다.")
    return evidence


def request_model_result(messages: list[dict[str, str]]) -> tuple[str, str | None]:
    response = request_json(
        "POST",
        CPU_PORT,
        CPU_PATH,
        payload={"messages": messages, "temperature": 0, "max_tokens": 120},
        timeout=120,
    )
    try:
        choice = response["choices"][0]
        content = choice["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise WorkflowLinkError("모델 응답에 choices[0].message.content가 없습니다.") from error
    if not isinstance(content, str) or not content.strip():
        raise WorkflowLinkError("모델이 빈 문자열을 반환했습니다.")
    return content, choice.get("finish_reason")


def draft_with_cpu(processed_text: str, review_rules: str) -> str:
    if not processed_text.strip() or not review_rules.strip():
        raise WorkflowLinkError("정리 결과와 검토 기준을 모두 넣으세요.")
    if len(processed_text) > 400 or len(review_rules) > 400:
        raise WorkflowLinkError("이 실습에서는 정리 결과와 검토 기준을 각각 400자 이내로 넣으세요.")
    return _complete_draft([
        {"role": "system", "content": "한국어 확인용 초안을 작성합니다. 자료에 없는 사실을 추가하지 마세요."},
        {"role": "user", "content": f"정리 결과\n{processed_text}\n\n검토 기준\n{review_rules}"},
    ])


def draft_with_evidence(processed_text: str, query: str, evidence: list[dict]) -> str:
    if not evidence:
        raise WorkflowLinkError("검색 결과 0건. 모델을 호출하지 않았습니다.")
    passages = []
    for item in evidence:
        passages.append(f"{item['file']} · {item['paragraph']}문단\n{item['excerpt']}")
    references = "\n\n".join(passages)
    return _complete_draft([
        {"role": "system", "content": "업무 자료와 검색 문단을 근거로 질문에 맞는 한국어 한 문장을 작성하세요. 원문에 없는 사실을 추가하지 마세요."},
        {"role": "user", "content": f"질문\n{query}\n\n업무 자료\n{processed_text}\n\n검색 문단\n{references}"},
    ])


def _complete_draft(messages: list[dict[str, str]]) -> str:
    content, finish_reason = request_model_result(messages)
    if finish_reason == "length":
        raise WorkflowLinkError("모델의 출력 길이 한도에 도달했습니다. 초안 요청을 한 문장으로 줄이세요.")
    return content.strip()
