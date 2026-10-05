# 本檔案功能：作為 Career Agent 統一入口，從 Terminal 接收 JD 並建立履歷生成 Context。

import sys

from Agents.Career.jd_parser import parse_jd
from Agents.Career.candidate_matcher import match_candidate
from Agents.Career.career_bridge import build_context, save_context


def read_jd():
    print("=== Career Agent ===")
    print()
    print("Paste JD below. Press Ctrl+D when finished.")
    print()

    data = sys.stdin.buffer.read()
    return data.decode("utf-8", errors="replace").strip()


def main():
    content = read_jd()

    if not content:
        raise ValueError("JD content is empty.")

    jd = parse_jd(content=content)
    result = match_candidate(jd)

    context = build_context(
        jd=jd,
        match_result=result,
    )

    output = save_context(context)

    print()
    print("=== Career Pipeline ===")
    print(f"JD       : {jd['job_title']}")
    print(f"Matched  : {len(result['matched_keywords'])}")
    print(f"Blocked  : {len(result['unmatched_keywords'])}")
    print(f"Context  : {output}")
    print("Status   : OK")


if __name__ == "__main__":
    main()
