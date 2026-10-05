"""Semantic Repository Boundary Guard for Career Agent.

Enforces the transition boundary rule:
1. PUBLIC SOURCE writes -> permitted only for intentional source-code/test/doc development
2. PRIVATE RUNTIME writes inside repository -> BLOCK (fail closed)
3. Legacy PRIVATE reads -> temporarily ALLOW + DEPRECATION WARNING
4. External workspace reads/writes -> ALLOW

Private runtime categories include at minimum:
- knowledge / identity
- resumes
- jd
- outputs
- cache
- logs
- runtime drafts / qa artifacts
- credentials / tokens
"""

import os
import warnings
from pathlib import Path
from typing import Optional, Union

CAREER_DIR = Path(__file__).resolve().parent


def find_repo_root(start_path: Optional[Union[str, Path]] = None) -> Path:
    """Find git repository root by locating .git directory upwards."""
    current = Path(start_path or CAREER_DIR).resolve()
    for parent in [current] + list(current.parents):
        if (parent / ".git").exists():
            return parent
    # Fallback to AI workspace root (two levels up from Agents/Career)
    if len(CAREER_DIR.parents) >= 2:
        return CAREER_DIR.parents[1]
    return CAREER_DIR.parent


REPO_ROOT = find_repo_root()


class RepositoryBoundaryViolationError(PermissionError):
    """Raised when an attempt is made to write private runtime artifacts inside repository boundary."""

    pass


# Private runtime filename patterns
PRIVATE_FILENAMES = {
    "identity.md",
    "experience.md",
    "skills.md",
    "jd.md",
    "jd_analysis.md",
    "evidence_mapping.yaml",
    "resume_strategy.yaml",
    "resume_strategy.md",
    "metadata.yaml",
    "local_jd_cache.json",
    "pipeline_logs.jsonl",
    "token.json",
    "credentials.json",
    "resume.md",
    "resume_index.md",
    "qa_report.md",
    "qa_result.yaml",
    "generation_metadata.yaml",
}

# Explicit public source files located in runtime/ that are code/specs
PUBLIC_RUNTIME_EXCEPTIONS = {
    "readme.md",
    "matching_schema.yaml",
    "strategy_schema.yaml",
    "canva_design_spec.md",
    "resume_one_page_spec.md",
    "antigravity_context.md",
}


def is_repo_path(path: Union[str, Path]) -> bool:
    """Check if the path resolves inside the repository root."""
    try:
        resolved = Path(path).resolve()
        return resolved == REPO_ROOT or REPO_ROOT in resolved.parents
    except Exception:
        return False


def classify_artifact(path: Union[str, Path]) -> str:
    """Classify target path into EXTERNAL, PUBLIC_SOURCE, or PRIVATE_RUNTIME.

    Returns:
        "EXTERNAL": Path resides outside Git repository.
        "PUBLIC_SOURCE": Path is within Git repository and represents legitimate source code,
                         tests, configuration, or documentation.
        "PRIVATE_RUNTIME": Path is within Git repository and represents private user data,
                           generated resumes, credentials, cache, or runtime logs.
    """
    if not is_repo_path(path):
        return "EXTERNAL"

    resolved = Path(path).resolve()
    try:
        rel_to_career = resolved.relative_to(CAREER_DIR)
        rel_str = str(rel_to_career).replace("\\", "/").lower()
    except ValueError:
        # Inside repo but outside Agents/Career
        rel_str = str(resolved.relative_to(REPO_ROOT)).replace("\\", "/").lower()

    filename = resolved.name.lower()

    # 1. Output directory artifacts (everything under output/ is private runtime)
    if rel_str.startswith("output/") or "/output/" in f"/{rel_str}":
        return "PRIVATE_RUNTIME"

    # 2. Knowledge directory artifacts (identity, experience, skills)
    if rel_str.startswith("knowledge/") or "/knowledge/" in f"/{rel_str}":
        return "PRIVATE_RUNTIME"

    # 3. Credentials and tokens
    if (
        rel_str.startswith("google/token.json")
        or rel_str.startswith("google/credentials.json")
        or filename in {"token.json", "credentials.json"}
        or "/credentials/" in f"/{rel_str}"
        or "/tokens/" in f"/{rel_str}"
    ):
        return "PRIVATE_RUNTIME"

    # 4. Logs and runtime caches
    if (
        rel_str == "runtime/pipeline/pipeline_logs.jsonl"
        or rel_str == "runtime/jd_matching/local_jd_cache.json"
        or filename.endswith("logs.jsonl")
        or filename.endswith("cache.json")
    ):
        return "PRIVATE_RUNTIME"

    # 5. Public runtime exceptions (specs/docs inside runtime/)
    if rel_str.startswith("runtime/") and filename in PUBLIC_RUNTIME_EXCEPTIONS:
        return "PUBLIC_SOURCE"

    # 6. Runtime drafts and QA output
    if rel_str.startswith("runtime/r7_3_draft/"):
        return "PRIVATE_RUNTIME"
    if rel_str.startswith("runtime/r7_4_qa/"):
        return "PRIVATE_RUNTIME"

    # 7. Specific private filename matches (e.g. resume_en.md, JD.md)
    if filename in PRIVATE_FILENAMES:
        return "PRIVATE_RUNTIME"
    if filename.startswith("resume_") and filename.endswith((".md", ".docx", ".pdf")):
        return "PRIVATE_RUNTIME"

    # 8. Otherwise, source code, test files, configs, and documentation
    return "PUBLIC_SOURCE"


def guard_write(path: Union[str, Path], caller_context: str = "") -> bool:
    """Enforce boundary guard on write operations.

    - EXTERNAL: Allowed.
    - PUBLIC_SOURCE: Allowed for intentional development.
    - PRIVATE_RUNTIME: BLOCKED (raises RepositoryBoundaryViolationError).
    """
    category = classify_artifact(path)
    if category == "EXTERNAL" or category == "PUBLIC_SOURCE":
        return True

    context_str = f" in context '{caller_context}'" if caller_context else ""
    raise RepositoryBoundaryViolationError(
        f"BLOCK: Repository Boundary Guard blocked private runtime write{context_str} "
        f"to in-tree path: '{path}'. "
        "Private runtime artifacts (knowledge, resumes, JD, outputs, cache, logs, tokens) "
        "must be written to an external workspace (use CAREER_WORKSPACE or --workspace)."
    )


def guard_read(path: Union[str, Path], caller_context: str = "") -> bool:
    """Enforce boundary guard on read operations.

    - EXTERNAL / PUBLIC_SOURCE: Allowed.
    - PRIVATE_RUNTIME: Temporarily ALLOWED with explicit DEPRECATION WARNING.
    """
    category = classify_artifact(path)
    if category == "PRIVATE_RUNTIME":
        context_str = f" during '{caller_context}'" if caller_context else ""
        warnings.warn(
            f"[DEPRECATION WARNING] Legacy private runtime read{context_str} "
            f"from in-tree repository path '{path}'. "
            "In-tree private files are deprecated and will be removed in open source distribution. "
            "Please configure CAREER_WORKSPACE or --workspace.",
            DeprecationWarning,
            stacklevel=2,
        )
    return True
