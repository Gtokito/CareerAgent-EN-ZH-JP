# 本檔案功能：定義 Antigravity 與 Career Agent 之間的輸入、分析、履歷生成與 Canva 工作流程契約。
# Career Pipeline Contract

## Purpose

Career Agent receives a job description from Antigravity and prepares
verified resume-generation context for Antigravity.

Career Agent does not generate the final visual resume.
Career Agent does not modify Canva files.

---

## Input

Antigravity may provide either:

### JD Text

Raw job description text pasted directly by the user.

### JD URL

A publicly accessible job-posting URL.

The input must contain either JD text or a JD URL.

Career Agent must never require `jd_input.md` or any manually edited
local JD input file.

---

## Processing

Career Agent performs:

1. Parse the job description.
2. Identify:
   - Job title
   - Responsibilities
   - Requirements
   - Keywords
3. Compare the JD against verified Career Knowledge.
4. Identify:
   - Must Highlight
   - Do Not Invent
5. Build a Resume Generation Context.

---

## Candidate Evidence

Candidate evidence must come only from:

- `Agents/Career/knowledge/identity.md`
- `Agents/Career/knowledge/experience.md`
- `Agents/Career/knowledge/skills.md`

Career Agent must not invent:

- Experience
- Responsibilities
- Achievements
- Metrics
- Certifications
- Education
- Technologies
- Industry experience
- Years of experience
- Language proficiency

---

## Output

Career Agent produces a runtime context for Antigravity containing:

### JD Profile

- Job title
- Responsibilities
- Requirements
- Keywords

### Candidate Match

- Matched evidence
- Must Highlight
- Do Not Invent

### Resume Generation Requirements

Generate:

1. English Resume
2. Traditional Chinese Resume
3. Japanese Resume

All three versions must preserve factual consistency.

---

## Antigravity Responsibilities

Antigravity is responsible for:

1. Generating the three-language resume content.
2. Reviewing factual consistency against Career Context.
3. Presenting the generated resumes for human review.
4. Using the user's existing Canva resume example as the visual template.

---

## Canva Workflow

Antigravity must:

1. Never modify the original Canva example.
2. Create a copy of the existing example.
3. Replace the resume content with the generated content.
4. Preserve the useful visual structure of the example.
5. Keep the resulting resume editable.
6. Present the result to the user for final manual adjustment.

---

## Human Approval

The final resume is always subject to human review.

Career Agent and Antigravity must never claim unverified candidate
experience merely because it appears in the JD.

When evidence is missing or uncertain, the information must remain
unverified and must not be presented as candidate experience.

---

## File Documentation Rule

Every Career source file must begin with a Traditional Chinese comment
or Markdown comment describing the purpose of that file.
