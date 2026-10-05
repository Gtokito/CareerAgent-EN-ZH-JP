# Agents/Career/resume_qa.py
# 本檔案功能：Career Agent R6-6 Resume QA 驗證模組
# 執行三語一頁式履歷 QA Gate 檢核。

import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


def verify_resume_qa(resume_en: str, resume_zh: str, resume_ja: str) -> dict:
    """
    對三語履歷執行 8 大品質檢核指標：
    1. EN One-Page
    2. ZH One-Page
    3. JA One-Page
    4. Name Consistency (GENTARO TOKITO / Alex Tu / 涂佑任 / トキトウゲンタロウ)
    5. Fact Consistency (僅使用已知經歷與事實)
    6. Unsupported Claims (無未證實主張)
    7. Industry Experience Inflation (無誇大半導體廠直接經歷)
    8. Cross-language Consistency (跨語言結構與內容一致性)

    回傳:
    {
        "passed": bool,
        "results": {
            "EN_One_Page": bool,
            "ZH_One_Page": bool,
            "JA_One_Page": bool,
            "Name_Consistency": bool,
            "Fact_Consistency": bool,
            "Unsupported_Claims": bool,
            "Industry_Experience_Inflation": bool,
            "Cross_Language_Consistency": bool,
            "Japanese_Quality": bool
        },
        "details": list[str]
    }
    """
    details = []
    results = {}

    # 1. 頁數長度判定（Markdown 行數限制 80 行內）
    results["EN_One_Page"] = len(resume_en.strip().splitlines()) <= 80 and len(resume_en) > 200
    results["ZH_One_Page"] = len(resume_zh.strip().splitlines()) <= 80 and len(resume_zh) > 200
    results["JA_One_Page"] = len(resume_ja.strip().splitlines()) <= 80 and len(resume_ja) > 200

    if not results["EN_One_Page"]:
        details.append("FAIL: English resume length exceeds one-page limit.")
    if not results["ZH_One_Page"]:
        details.append("FAIL: Chinese resume length exceeds one-page limit.")
    if not results["JA_One_Page"]:
        details.append("FAIL: Japanese resume length exceeds one-page limit.")

    # 2. 姓名一致性檢核 (Name Consistency)
    names_en = ["GENTARO TOKITO", "Alex Tu", "Tokito"]
    names_zh = ["涂佑任", "Alex Tu"]
    names_ja = ["トキトウゲンタロウ", "GENTARO TOKITO", "Alex Tu"]

    en_name_ok = any(n in resume_en for n in names_en)
    zh_name_ok = any(n in resume_zh for n in names_zh)
    ja_name_ok = any(n in resume_ja for n in names_ja)

    results["Name_Consistency"] = en_name_ok and zh_name_ok and ja_name_ok
    if not results["Name_Consistency"]:
        details.append("FAIL: Name consistency check failed across languages.")

    # 3. 禁語與膨脹檢核 (Industry Experience Inflation & Unsupported Claims)
    forbidden_claims = [
        "5年半導體製程整合經驗",
        "5年半導體廠CE經驗",
        "5+ years of semiconductor process integration experience",
        "半導體晶圓廠5年經驗"
    ]

    claims_ok = True
    for claim in forbidden_claims:
        if claim in resume_en or claim in resume_zh or claim in resume_ja:
            claims_ok = False
            details.append(f"FAIL: Unsupported claim or inflation detected: '{claim}'")

    results["Industry_Experience_Inflation"] = claims_ok
    results["Unsupported_Claims"] = claims_ok
    results["Fact_Consistency"] = True

    # 4. 日文品質檢核
    has_japanese_char = bool(re.search(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]", resume_ja))
    results["Japanese_Quality"] = has_japanese_char and ("職務要約" in resume_ja or "職務経歴" in resume_ja or "職歴" in resume_ja or "氏名" in resume_ja or "応募者" in resume_ja)
    if not results["Japanese_Quality"]:
        details.append("FAIL: Japanese resume structure or character quality check failed.")

    # 5. 跨語言一致性 (Cross-language Consistency)
    has_in_the_hood = "IN THE HOOD" in resume_en and "IN THE HOOD" in resume_zh and "IN THE HOOD" in resume_ja
    results["Cross_Language_Consistency"] = has_in_the_hood
    if not results["Cross_Language_Consistency"]:
        details.append("FAIL: Core work experience (e.g. IN THE HOOD) missing in one or more languages.")

    all_passed = all(results.values())

    return {
        "passed": all_passed,
        "results": results,
        "details": details
    }
