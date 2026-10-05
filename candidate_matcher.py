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
    "python": [
        "python",
    ],
    "自動化": [
        "automation",
        "automated",
        "自動化",
    ],
    "治理": [
        "governance",
        "governor",
        "治理",
    ],
    "雲端": [
        "cloud",
        "aws",
        "google cloud",
        "kubernetes",
        "docker",
        "雲端",
    ],
    "ai": [
        "ai",
        "agent",
        "llm",
        "machine learning",
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
    target_dir = KNOWLEDGE
    source_label = "knowledge"
    if not target_dir.exists() or not list(target_dir.glob("*.md")):
        fallback = BASE / "examples" / "sample_profile"
        if fallback.exists() and list(fallback.glob("*.md")):
            target_dir = fallback
            source_label = "examples/sample_profile (Fallback Demo)"

    files = list(target_dir.glob("*.md"))
    content = "\n".join(path.read_text(encoding="utf-8") for path in files).lower()
    return content, source_label


def match_candidate(jd):
    knowledge, source_label = load_knowledge()
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
        "source": source_label,
        "matched_keywords": matched,
        "transferable_keywords": transferable,
        "unmatched_keywords": blocked,
    }


if __name__ == "__main__":
    print("=" * 60)
    print("🎯 Career Agent: Candidate Matcher Demo")
    print("=" * 60)

    demo_jd = {
        "job_title": "Senior AI Platform & Automation Engineer",
        "raw_text": "Seeking an engineer with strong verification, python standardization, english communication, and sop skills.",
        "keywords": ["AI", "Python", "自動化", "雲端", "治理", "英文", "半導體"]
    }


    result = match_candidate(demo_jd)
    print(f"📌 目標職缺: {result['job_title']}")
    print(f"📂 候選人經歷庫: {result['source']}")
    print("-" * 60)
    print(f"✅ 精確匹配能力 (Matched):      {result['matched_keywords']}")
    print(f"🔄 可轉移能力 (Transferable):  {result['transferable_keywords']}")
    print(f"⛔ 阻擋/不可虛構 (Blocked):    {result['unmatched_keywords']}")
    print("=" * 60)
    print("✨ 匹配分析完成！開箱即用運作正常。")

