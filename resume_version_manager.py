# Agents/Career/resume_version_manager.py
# 本檔案功能：Career Agent R6-6 履歷版本管理模組
# 採用 Company -> Position -> Version_ID 階層架構，並管理 is_latest 狀態與 resume_index.md。

import datetime
from pathlib import Path
import re
import yaml

BASE_DIR = Path(__file__).resolve().parent

from Agents.Career.workspace import resolve_workspace
from Agents.Career.boundary_guard import guard_write, guard_read


def get_output_dir() -> Path:
    return resolve_workspace().output_dir


class DynamicOutputDir:
    def __truediv__(self, other):
        return get_output_dir() / other

    def __fspath__(self):
        return str(get_output_dir())

    def __str__(self):
        return str(get_output_dir())

    def __repr__(self):
        return repr(get_output_dir())

    def __getattr__(self, name):
        return getattr(get_output_dir(), name)


OUTPUT_DIR = DynamicOutputDir()


def sanitize_name(name: str) -> str:
    """清理公司名稱或職位名稱，使其適合做為資料夾名稱"""
    if not name:
        return "Unknown"
    # 將非英數中文字元及空白轉為下劃線
    clean = re.sub(r"[^\w\u4e00-\u9fff\u3040-\u30ff\u31f0-\u31ff]", "_", name.strip())
    clean = re.sub(r"_+", "_", clean)
    return clean.strip("_") or "Unknown"


def get_next_version_id(company: str, position: str, target_date: str = None) -> str:
    """
    依據公司與職位產生唯一的 Version ID。
    格式: YYYYMMDD_v01, YYYYMMDD_v02 ...
    """
    if not target_date:
        target_date = datetime.datetime.now().strftime("%Y%m%d")

    clean_company = sanitize_name(company)
    clean_position = sanitize_name(position)
    position_dir = OUTPUT_DIR / clean_company / clean_position

    if not position_dir.exists():
        return f"{target_date}_v01"

    pattern = re.compile(rf"^{target_date}_v(\d+)$")
    max_num = 0

    for item in position_dir.iterdir():
        if item.is_dir():
            match = pattern.match(item.name)
            if match:
                num = int(match.group(1))
                if num > max_num:
                    max_num = num

    next_num = max_num + 1
    return f"{target_date}_v{next_num:02d}"


def migrate_legacy_if_needed() -> Path:
    """
    將既有 output/ 目錄下的履歷轉存至 output/Legacy/
    如果 Legacy/ 已經存在則不再重複執行。
    """
    legacy_dir = OUTPUT_DIR / "Legacy"
    legacy_dir.mkdir(parents=True, exist_ok=True)

    legacy_metadata_path = legacy_dir / "metadata.yaml"
    if legacy_metadata_path.exists():
        return legacy_dir

    # 檢查 output/ 根目錄下的既有檔案
    legacy_files = []
    for filename in ["resume_en.md", "resume_zh.md", "resume_ja.md"]:
        src = OUTPUT_DIR / filename
        if src.exists() and src.is_file():
            dst = legacy_dir / filename
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            legacy_files.append(filename)

    # 產生 Legacy 的 metadata.yaml
    metadata = {
        "version_id": "Legacy",
        "company": "UNKNOWN",
        "position": "UNKNOWN",
        "created_at": datetime.datetime.now().isoformat(),
        "status": "ARCHIVED",
        "is_latest": False,
        "source_jd": "UNKNOWN",
        "languages": ["en", "zh", "ja"],
        "resume_files": legacy_files if legacy_files else ["resume_en.md", "resume_zh.md", "resume_ja.md"]
    }

    with open(legacy_metadata_path, "w", encoding="utf-8") as f:
        yaml.dump(metadata, f, allow_unicode=True, sort_keys=False)

    return legacy_dir


def update_index_md(entry: dict):
    """
    更新 output/resume_index.md，紀錄最新的履歷版本狀態（最新紀錄置頂）。
    entry 結構:
    {
        "company": str,
        "position": str,
        "version": str,
        "date": str,
        "status": str,
        "is_latest": str ("YES" or "NO"),
        "languages": str,
        "gdocs": str,
        "jd": str
    }
    """
    index_file = OUTPUT_DIR / "resume_index.md"
    header = "# Career Agent Resume Version Index\n\n"
    table_header = "| Company | Position | Version | Date | Status | Latest | Languages | Google Docs | JD |\n|---|---|---|---|---|---|---|---|---|\n"

    existing_rows = []
    if index_file.exists():
        content = index_file.read_text(encoding="utf-8")
        lines = content.splitlines()
        for line in lines:
            if line.startswith("|") and not line.startswith("| Company") and not line.startswith("|---"):
                if entry.get("is_latest") == "YES" and f"| {entry['company']} | {entry['position']} |" in line:
                    # 更新同一公司職位的舊紀錄 Latest 欄位為 NO
                    updated_line = line.replace("| YES |", "| NO |")
                    existing_rows.append(updated_line)
                else:
                    existing_rows.append(line)

    new_row = f"| {entry['company']} | {entry['position']} | {entry['version']} | {entry['date']} | {entry['status']} | {entry['is_latest']} | {entry['languages']} | {entry['gdocs']} | {entry['jd']} |"

    # 移除相同 company, position, version 的舊紀錄（如有）
    filtered_rows = [r for r in existing_rows if not (f"| {entry['company']} | {entry['position']} | {entry['version']} |" in r)]
    all_rows = [new_row] + filtered_rows

    index_content = header + table_header + "\n".join(all_rows) + "\n"
    index_file.write_text(index_content, encoding="utf-8")


def save_version(
    company: str,
    position: str,
    version_id: str,
    jd_text: str,
    resume_en: str,
    resume_zh: str,
    resume_ja: str,
    qa_passed: bool,
    gdocs_links: dict = None,
    source_stage: str = "R7-3",
    qa_stage: str = "R7-4",
    qa_status: str = "PASS"
) -> dict:
    """
    依據 QA PASS/FAIL 建立或更新版本資料夾。
    1. 若 QA PASS:
       - 建立 output/<Company>/<Position>/<Version_ID>/
       - 寫入 JD.md, resume_en.md, resume_zh.md, resume_ja.md, metadata.yaml (status: FINAL, is_latest: True)
       - 將該 Position 下舊版本的 metadata.yaml 改為 is_latest: False
       - 更新 resume_index.md
    2. 若 QA FAIL:
       - 寫入 output/<Company>/<Position>/<Version_ID>/ 但標記 status: QA_FAIL, is_latest: False
       - 不修改既有 FINAL 版本與 is_latest 狀態
    """
    clean_company = sanitize_name(company)
    clean_position = sanitize_name(position)
    position_dir = OUTPUT_DIR / clean_company / clean_position
    version_dir = position_dir / version_id
    guard_write(version_dir / "JD.md", caller_context="save_version")
    version_dir.mkdir(parents=True, exist_ok=True)

    # 寫入檔案
    (version_dir / "JD.md").write_text(jd_text, encoding="utf-8")
    (version_dir / "resume_en.md").write_text(resume_en, encoding="utf-8")
    (version_dir / "resume_zh.md").write_text(resume_zh, encoding="utf-8")
    (version_dir / "resume_ja.md").write_text(resume_ja, encoding="utf-8")

    status = "FINAL" if qa_passed else "QA_FAIL"
    is_latest = qa_passed

    if qa_passed:
        # 將同一 Position 下其他的舊版本改為 is_latest: False
        for v_dir in position_dir.iterdir():
            if v_dir.is_dir() and v_dir.name != version_id:
                meta_file = v_dir / "metadata.yaml"
                if meta_file.exists():
                    try:
                        with open(meta_file, "r", encoding="utf-8") as f:
                            m_data = yaml.safe_load(f) or {}
                        m_data["is_latest"] = False
                        with open(meta_file, "w", encoding="utf-8") as f:
                            yaml.dump(m_data, f, allow_unicode=True, sort_keys=False)
                    except Exception as e:
                        print(f"Warning: Failed to update metadata in {meta_file}: {e}")

    gdocs_str = "N/A"
    if gdocs_links:
        gdocs_str = f"EN: {gdocs_links.get('EN', 'N/A')}, ZH: {gdocs_links.get('ZH', 'N/A')}, JA: {gdocs_links.get('JA', 'N/A')}"

    metadata = {
        "version_id": version_id,
        "company": company,
        "position": position,
        "created_at": datetime.datetime.now().isoformat(),
        "status": status,
        "source_stage": source_stage,
        "qa_stage": qa_stage,
        "qa_status": qa_status if qa_passed else "FAIL",
        "is_latest": is_latest,
        "source_jd": "JD.md",
        "languages": ["en", "zh", "ja"],
        "resume_files": ["resume_en.md", "resume_zh.md", "resume_ja.md"],
        "gdocs_links": gdocs_links or {}
    }

    metadata_path = version_dir / "metadata.yaml"
    with open(metadata_path, "w", encoding="utf-8") as f:
        yaml.dump(metadata, f, allow_unicode=True, sort_keys=False)

    # 更新索引檔
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    index_entry = {
        "company": company,
        "position": position,
        "version": version_id,
        "date": today_str,
        "status": status,
        "is_latest": "YES" if is_latest else "NO",
        "languages": "EN, ZH, JA",
        "gdocs": gdocs_str,
        "jd": "JD.md"
    }
    update_index_md(index_entry)

    return {
        "version_dir": str(version_dir),
        "version_id": version_id,
        "status": status,
        "is_latest": is_latest,
        "metadata": metadata
    }
