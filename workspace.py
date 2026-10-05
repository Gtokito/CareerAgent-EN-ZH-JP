"""Workspace Resolver and Management for Career Agent.

Implements the four-tier workspace precedence hierarchy:
1. CLI argument: --workspace <path>
2. Environment variable: CAREER_WORKSPACE
3. External default workspace: ~/.career
4. Legacy in-tree fallback: Agents/Career (READ-ONLY with explicit deprecation warning)
"""

import os
import sys
import warnings
from pathlib import Path
from typing import Optional, Union

# Define repository root and legacy in-tree path
CAREER_MODULE_DIR = Path(__file__).resolve().parent
REPO_ROOT = CAREER_MODULE_DIR.parents[1] if len(CAREER_MODULE_DIR.parents) >= 2 else CAREER_MODULE_DIR.parent
DEFAULT_EXTERNAL_WORKSPACE = Path(os.path.expanduser("~/.career"))


class CareerWorkspace:
    """Represents a resolved Career Agent workspace with standard subdirectories."""

    def __init__(self, root: Path, source: str, is_legacy: bool = False):
        self.root = Path(root).resolve()
        self.source = source
        self.is_legacy = is_legacy

    @property
    def knowledge_dir(self) -> Path:
        return self.root / "knowledge"

    @property
    def output_dir(self) -> Path:
        return self.root / "output"

    @property
    def runtime_dir(self) -> Path:
        return self.root / "runtime"

    @property
    def cache_dir(self) -> Path:
        return self.root / "runtime" / "cache"

    @property
    def logs_file(self) -> Path:
        return self.root / "runtime" / "pipeline" / "pipeline_logs.jsonl"

    @property
    def credentials_dir(self) -> Path:
        return self.root / "google"

    @property
    def token_path(self) -> Path:
        return self.credentials_dir / "token.json"

    def ensure_dirs(self) -> None:
        """Create standard workspace directory structure if not legacy."""
        if self.is_legacy:
            return
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.runtime_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        (self.runtime_dir / "pipeline").mkdir(parents=True, exist_ok=True)
        self.credentials_dir.mkdir(parents=True, exist_ok=True)

    def resolve_knowledge_file(self, filename: str) -> Path:
        """Resolve a knowledge file from workspace knowledge dir, with legacy fallback read."""
        target = self.knowledge_dir / filename
        if target.exists():
            return target

        # If not present in active external workspace, check legacy in-tree knowledge
        legacy_target = CAREER_MODULE_DIR / "knowledge" / filename
        if legacy_target.exists():
            warnings.warn(
                f"[DEPRECATION WARNING] Knowledge file '{filename}' resolved from legacy in-tree repository path. "
                "In-tree private data will be removed in open source release. "
                f"Please migrate knowledge files to active workspace: {self.knowledge_dir}",
                DeprecationWarning,
                stacklevel=2,
            )
            return legacy_target

        return target

    def resolve_output_dir(self, company: str, position: str, version_id: str) -> Path:
        """Return version directory under active workspace output."""
        return self.output_dir / company / position / version_id

    def __repr__(self) -> str:
        return f"<CareerWorkspace root={self.root} source={self.source} is_legacy={self.is_legacy}>"


def resolve_workspace(
    cli_workspace: Optional[Union[str, Path]] = None,
    env_var_name: str = "CAREER_WORKSPACE",
    allow_legacy_fallback: bool = True,
    prefer_external_default: bool = False,
) -> CareerWorkspace:
    """Resolve active CareerWorkspace according to strict precedence rules.

    Precedence:
    1. CLI --workspace (cli_workspace argument)
    2. CAREER_WORKSPACE environment variable
    3. External default workspace (~/.career_workspace) if prefer_external_default or exists
    4. Legacy in-tree fallback (READ-ONLY, with explicit deprecation warning)
    """
    # 1. CLI precedence
    if cli_workspace is not None and str(cli_workspace).strip():
        ws_path = Path(cli_workspace).expanduser().resolve()
        return CareerWorkspace(root=ws_path, source="CLI", is_legacy=False)

    # 2. ENV precedence
    env_val = os.environ.get(env_var_name, "").strip()
    if env_val:
        ws_path = Path(env_val).expanduser().resolve()
        return CareerWorkspace(root=ws_path, source="ENV", is_legacy=False)

    # 3. External default workspace
    if prefer_external_default or DEFAULT_EXTERNAL_WORKSPACE.exists() or not allow_legacy_fallback:
        return CareerWorkspace(root=DEFAULT_EXTERNAL_WORKSPACE.resolve(), source="DEFAULT", is_legacy=False)

    # 4. Legacy in-tree fallback
    warnings.warn(
        "[DEPRECATION WARNING] No external workspace specified (--workspace or CAREER_WORKSPACE). "
        "Falling back to legacy in-tree repository workspace. "
        "Private runtime writes inside the repository will be blocked by Repository Boundary Guard. "
        f"Please configure an external workspace (e.g. {DEFAULT_EXTERNAL_WORKSPACE}).",
        DeprecationWarning,
        stacklevel=2,
    )
    return CareerWorkspace(root=CAREER_MODULE_DIR, source="LEGACY_FALLBACK", is_legacy=True)
