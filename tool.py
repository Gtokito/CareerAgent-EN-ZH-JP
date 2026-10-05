# Agents/Career/tool.py
# 本檔案功能：Career Agent 對外標準工具 Gateway（具備防禦性物件轉字典功能）。

import os
from typing import Dict, Any, Optional
from Agents.Career.runtime.jd_matching.jd_parser import fetch_jd_from_url
from Agents.Career.run_career_pipeline import execute_career_pipeline

def run_career_agent_tool(url: str, dry_run: bool = True, email_context: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    print(f"[CareerTool] Initiating pipeline for URL: {url}")
    
    if type(dry_run) is not bool:
        return {"status": "FAILED", "failure_reason": "dry_run must be a boolean."}

    # 1. 取得 JD 內容；失敗不得進入生成管線。
    try:
        res = fetch_jd_from_url(url, email_context=email_context)
    except Exception as e:
        return {"status": "FAILED", "failure_reason": f"JD fetch failed: {e}"}
    if not isinstance(res, dict) or res.get("success") is not True:
        return {
            "status": "FAILED",
            "failure_reason": res.get("error") or "JD unavailable" if isinstance(res, dict) else "Invalid JD response"
        }
    if not all(isinstance(res.get(key), str) and res[key].strip()
               for key in ("company", "position", "jd_text")):
        return {"status": "FAILED", "failure_reason": "Incomplete or invalid JD response."}
    company = res.get("company", "Target Company")
    position = res.get("position", "Target Position")
    jd_text = res.get("jd_text", "")

    if not jd_text:
        return {
            "status": "FAILED",
            "failure_reason": "Fetched JD text is empty."
        }

    # 2. 執行底層管線並安全轉譯回傳物件為標準字典
    try:
        pipeline_res = execute_career_pipeline(
            company=company,
            position=position,
            jd_text=jd_text,
            skip_google_publishing=dry_run
        )
        
        # 防禦性將 PipelineResult 物件轉換為 Dict
        if hasattr(pipeline_res, "__dict__"):
            res_dict = dict(pipeline_res.__dict__)
        elif isinstance(pipeline_res, dict):
            res_dict = pipeline_res
        else:
            return {"status": "FAILED", "failure_reason": "Invalid pipeline result."}

        # 確保必要欄位存在
        if res_dict.get("status") not in ("SUCCESS", "FAILED", "ERROR"):
            return {"status": "FAILED", "failure_reason": "Missing or invalid pipeline status."}
        if "company" not in res_dict or not res_dict["company"]:
            res_dict["company"] = company
        if "position" not in res_dict or not res_dict["position"]:
            res_dict["position"] = position

        return res_dict

    except Exception as e:
        return {
            "status": "FAILED",
            "company": company,
            "position": position,
            "failure_reason": f"Pipeline exception: {e}"
        }
