"""Infrastructure for loading AI guard files from filesystem."""

from __future__ import annotations

from pathlib import Path

from praxis.domain.ai_guards import (
    EnvironmentConfig,
    GuardFile,
    GuardLevel,
)


def get_user_guards_dir() -> Path | None:
    """Get the user-level AI guards directory.

    Returns:
        Path to ~/.ai-guards/ if it exists, None otherwise
    """
    home = Path.home()
    guards_dir = home / ".ai-guards"
    return guards_dir if guards_dir.exists() else None


def get_project_guards_dir(project_path: Path | None = None) -> Path | None:
    """Get the project-level AI guards directory.

    Args:
        project_path: Path to project root (defaults to cwd)

    Returns:
        Path to praxis/ai-guards/ if it exists, None otherwise
    """
    if project_path is None:
        project_path = Path.cwd()

    guards_dir = project_path / "praxis" / "ai-guards"
    return guards_dir if guards_dir.exists() else None


def load_environment_config() -> EnvironmentConfig:
    """Load the active environment from user guards.

    Reads ~/.ai-guards/env.md to determine active environment.
    Defaults to 'home' if file doesn't exist or can't be parsed.

    Returns:
        EnvironmentConfig with active environment
    """
    user_guards_dir = get_user_guards_dir()
    if not user_guards_dir:
        return EnvironmentConfig(active_environment="home")

    env_file = user_guards_dir / "env.md"
    if not env_file.exists():
        return EnvironmentConfig(active_environment="home")

    # Parse env.md for active environment
    # Expected format: "ENV=work" or "ENV=home" somewhere in the file
    try:
        content = env_file.read_text(encoding="utf-8")
        # Look for ENV=work or ENV=home
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("ENV="):
                env_value = line.split("=", 1)[1].strip().lower()
                if env_value in ["home", "work"]:
                    return EnvironmentConfig(
                        active_environment=env_value,  # type: ignore[arg-type]
                        env_file_path=env_file,
                    )
    except Exception:
        pass

    return EnvironmentConfig(
        active_environment="home",
        env_file_path=env_file,
    )


def load_guard_file(
    path: Path,
    level: GuardLevel,
    domain: str | None = None,
) -> GuardFile:
    """Load a single guard file.

    Args:
        path: Path to the guard file
        level: Guard level (user_core, user_env, etc.)
        domain: Domain name for project-level guards

    Returns:
        GuardFile with content if exists
    """
    if not path.exists():
        return GuardFile(
            path=path,
            level=level,
            exists=False,
            domain=domain,
        )

    try:
        content = path.read_text(encoding="utf-8")
        return GuardFile(
            path=path,
            level=level,
            exists=True,
            content=content,
            domain=domain,
        )
    except Exception:
        return GuardFile(
            path=path,
            level=level,
            exists=False,
            domain=domain,
        )


def load_user_core_guard() -> GuardFile | None:
    """Load user core guard file.

    Returns:
        GuardFile if ~/.ai-guards/core.md exists, None otherwise
    """
    user_guards_dir = get_user_guards_dir()
    if not user_guards_dir:
        return None

    core_file = user_guards_dir / "core.md"
    guard = load_guard_file(core_file, GuardLevel.USER_CORE)
    return guard if guard.exists else None


def load_user_tools_guard() -> GuardFile | None:
    """Load user tools guard file.

    Returns:
        GuardFile if ~/.ai-guards/tools.md exists, None otherwise
    """
    user_guards_dir = get_user_guards_dir()
    if not user_guards_dir:
        return None

    tools_file = user_guards_dir / "tools.md"
    guard = load_guard_file(tools_file, GuardLevel.USER_TOOLS)
    return guard if guard.exists else None


def load_user_env_guard(environment: str) -> GuardFile | None:
    """Load user environment overlay guard file.

    Args:
        environment: 'home' or 'work'

    Returns:
        GuardFile if ~/.ai-guards/env/{environment}.md exists, None otherwise
    """
    user_guards_dir = get_user_guards_dir()
    if not user_guards_dir:
        return None

    env_file = user_guards_dir / "env" / f"{environment}.md"
    guard = load_guard_file(env_file, GuardLevel.USER_ENV)
    return guard if guard.exists else None


def load_project_domain_guards(
    domain: str,
    project_path: Path | None = None,
) -> list[GuardFile]:
    """Load project-level domain guard files.

    Args:
        domain: Domain name (code, create, write, etc.)
        project_path: Path to project root (defaults to cwd)

    Returns:
        List of GuardFile objects (may be empty if none exist)
    """
    guards_dir = get_project_guards_dir(project_path)
    if not guards_dir:
        return []

    # Look for {domain}.md
    domain_file = guards_dir / f"{domain}.md"
    guard = load_guard_file(domain_file, GuardLevel.PROJECT_DOMAIN, domain=domain)

    return [guard] if guard.exists else []


def discover_all_project_guards(
    project_path: Path | None = None,
) -> list[GuardFile]:
    """Discover all project-level guard files.

    Args:
        project_path: Path to project root (defaults to cwd)

    Returns:
        List of all project guard files found
    """
    guards_dir = get_project_guards_dir(project_path)
    if not guards_dir:
        return []

    guards = []
    for file_path in guards_dir.glob("*.md"):
        domain = file_path.stem  # filename without .md extension
        guard = load_guard_file(file_path, GuardLevel.PROJECT_DOMAIN, domain=domain)
        if guard.exists:
            guards.append(guard)

    return guards
