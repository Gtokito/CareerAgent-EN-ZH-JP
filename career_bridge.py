# 本檔案功能：將 JD、候選人匹配結果與證據限制組合成 Antigravity 履歷生成 Context。

from pathlib import Path


BASE = Path(__file__).resolve().parent
RUNTIME = BASE / "runtime"


def build_context(jd, match_result):
    def bullets(items):
        return "\n".join(f"- {x}" for x in items) if items else "- None"

    return f"""# Antigravity Resume Context

## Job

{jd["job_title"]}

## Responsibilities

{bullets(jd["responsibilities"])}

## Requirements

{bullets(jd["requirements"])}

## JD Keywords

{", ".join(jd["keywords"])}

## Evidence Classification

### Must Highlight

{bullets(match_result["matched_keywords"])}

These are JD-relevant concepts supported by candidate evidence.
They may be emphasized only when the underlying candidate evidence supports the exact claim.

### Transferable Strengths

{bullets(match_result.get("transferable_keywords", []))}

These indicate transferable knowledge or domain familiarity only.
NEVER rewrite them as previous job experience, semiconductor work experience,
technical manufacturing experience, or direct responsibility for the JD requirement.

### Do Not Invent

{bullets(match_result["unmatched_keywords"])}

These are explicitly prohibited as candidate experience.
They may only appear when describing the JD requirement itself.

## Candidate Evidence

Use only verified evidence from:

- Agents/Career/knowledge/identity.md
- Agents/Career/knowledge/experience.md
- Agents/Career/knowledge/skills.md

## Generation Rules

1. Use only verified candidate evidence.
2. Never convert a JD requirement into candidate experience.
3. Must Highlight items may be emphasized only when supported by matching evidence.
4. Transferable Strengths must be described only as transferable capabilities or domain familiarity.
5. Never describe Transferable Strengths as direct industry experience.
6. Never present Do Not Invent items as candidate experience.
7. Do not invent achievements, metrics, responsibilities, certifications, technologies, projects, or job history.
8. Adapt wording to the JD without changing factual meaning.
9. If a JD requirement is unsupported, do not manufacture evidence to improve the match.
10. Clearly preserve the distinction between candidate evidence and JD requirements.
11. Generate English Resume.
12. Generate 中文履歷.
13. Generate 日本語履歴書.
14. Prepare all outputs for human review and editing in Antigravity.
15. Canva customization is a later presentation step.
"""


def save_context(context):
    path = RUNTIME / "antigravity_context.md"
    path.write_text(context, encoding="utf-8")
    return path
