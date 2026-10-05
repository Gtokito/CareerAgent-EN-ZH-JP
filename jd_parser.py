# 本檔案功能：將 Antigravity 傳入的 JD 文字解析成 Career Agent 可使用的結構化資料。

import re


def parse_jd(content):
    content = content.strip()

    if not content:
        raise ValueError("JD content is empty.")

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    job_title = lines[0]

    responsibilities = []
    requirements = []

    section = None

    for line in lines[1:]:
        if "職務說明" in line:
            section = "responsibilities"
            continue

        if "需求條件" in line:
            section = "requirements"
            continue

        if section == "responsibilities":
            responsibilities.append(line)

        elif section == "requirements":
            requirements.append(line)

    keyword_pool = " ".join(lines)

    keyword_map = {
        "半導體": ["半導體", "semiconductor"],
        "整合": ["整合", "integration"],
        "製程": ["製程", "process"],
        "產品": ["產品", "product"],
        "schedule": ["schedule", "時程"],
        "驗證": ["驗證", "verification", "validate"],
    }

    keywords = [
        keyword
        for keyword, terms in keyword_map.items()
        if any(term.lower() in keyword_pool.lower() for term in terms)
    ]

    return {
        "job_title": job_title,
        "responsibilities": responsibilities,
        "requirements": requirements,
        "keywords": keywords,
        "raw_text": content,
    }
