# 本檔案功能：以直接證據、可轉移能力與不可虛構要求三層模型比對 JD 與候選人 Knowledge。

from pathlib import Path


BASE = Path(__file__).resolve().parent
KNOWLEDGE = BASE / "knowledge"


DIRECT_EVIDENCE = {
    "溝通": [
        "communication",
        "stakeholder",
        "cross-cultural",
        "溝通",
        "協調",
    ],
    "專案": [
        "project",
        "program",
        "project management",
        "專案",
    ],
    "產品": [
        "product",
        "產品",
        "customer",
        "客戶",
    ],
    "製程": [
        "process",
        "sop",
        "standardization",
        "流程",
        "標準化",
    ],
    "驗證": [
        "verification",
        "validate",
        "evaluation",
        "test",
        "驗證",
    ],
    "schedule": [
        "schedule",
        "time management",
        "時程",
    ],
    "英文": [
        "english",
        "英文",
    ],
    "日文": [
        "japanese",
        "日文",
    ],
}


INDUSTRY_TERMS = {
    "半導體": [
        "半導體",
        "semiconductor",
    ],
}


BLOCKED_TERMS = [
    "半導體廠ce",
    "製程整合",
    "產品工程",
    "pre-tapeout",
    "tape-out",
    "pilot run",
    "mass production",
    "wp/ap/wt/ft",
]


def load_knowledge():
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in KNOWLEDGE.glob("*.md")
    ).lower()


def match_candidate(jd):
    knowledge = load_knowledge()
    jd_text = jd.get("raw_text", "").lower()

    matched = []
    transferable = []
    blocked = []

    # 產業／專業職務要求必須與「實際工作經驗」分開處理。
    for term in BLOCKED_TERMS:
        if term in jd_text:
            blocked.append(term)

    for keyword in jd["keywords"]:
        key = keyword.lower()

        # 產業名稱不能直接視為候選人的工作經驗。
        if key in INDUSTRY_TERMS:
            if any(term in knowledge for term in INDUSTRY_TERMS[key]):
                transferable.append(keyword)
            continue

        terms = DIRECT_EVIDENCE.get(key, [key])

        if any(term in knowledge for term in terms):
            matched.append(keyword)

    return {
        "job_title": jd["job_title"],
        "matched_keywords": matched,
        "transferable_keywords": transferable,
        "unmatched_keywords": blocked,
    }


if __name__ == "__main__":
    print("Candidate Matcher: OK")
