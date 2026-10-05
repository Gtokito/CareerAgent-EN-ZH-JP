# 本檔案功能：定義 Antigravity 如何依據 Career Context 生成三語履歷並銜接 Canva 製作流程。

# Antigravity Resume Generation Prompt

## Input

Read:

Agents/Career/runtime/antigravity_context.md

Use only the verified candidate evidence specified by that Context.

## Outputs

Generate:

1. English Resume
2. 中文履歷
3. 日本語履歴書

Save to:

Agents/Career/output/resume_en.md
Agents/Career/output/resume_zh.md
Agents/Career/output/resume_ja.md

## Rules

1. Never invent candidate experience.
2. Never convert JD requirements into candidate experience.
3. Preserve the distinction between Must Highlight, Transferable Strengths, and Do Not Invent.
4. Use only verified evidence from Candidate Evidence.
5. Adapt wording to the target JD without changing factual meaning.
6. Prioritize relevant evidence rather than listing every skill.
7. Keep all three language versions factually consistent.
8. Prepare concise, professional resume content suitable for human review.
9. Do not generate final visual design inside the resume files.

## Canva Handoff

After human review:

1. Use the user's existing Canva resume example as the visual template.
2. Duplicate the existing Canva design rather than creating a new design from scratch.
3. Replace the template text with the approved resume content.
4. Preserve the original visual hierarchy unless content length requires adjustment.
5. Keep the final Canva version editable for human refinement.
