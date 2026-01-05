from __future__ import annotations

from pathlib import Path

from praxis.application.stage_service import transition_stage


def _write_praxis_yaml(project_root: Path, *, domain: str, stage: str) -> None:
    (project_root / "praxis.yaml").write_text(
        f"""domain: {domain}
stage: {stage}
privacy_level: personal
environment: Home
"""
    )


def test_stage_transition_creates_next_stage_doc(tmp_path: Path) -> None:
    _write_praxis_yaml(tmp_path, domain="code", stage="capture")

    result = transition_stage(tmp_path, "sense")
    assert result.success

    sense_doc = tmp_path / "docs" / "sense.md"
    assert sense_doc.exists()
    assert "# Sense" in sense_doc.read_text()


def test_stage_transition_does_not_overwrite_existing_stage_doc(tmp_path: Path) -> None:
    _write_praxis_yaml(tmp_path, domain="code", stage="capture")

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir(exist_ok=True)
    sense_doc = docs_dir / "sense.md"
    sense_doc.write_text("EXISTING")

    result = transition_stage(tmp_path, "sense")
    assert result.success

    assert sense_doc.read_text() == "EXISTING"


def test_create_transition_before_formalize_does_not_create_brief(
    tmp_path: Path,
) -> None:
    _write_praxis_yaml(tmp_path, domain="create", stage="capture")

    result = transition_stage(tmp_path, "sense")
    assert result.success

    brief_doc = tmp_path / "docs" / "brief.md"
    assert not brief_doc.exists()


def test_create_transition_to_formalize_creates_brief(tmp_path: Path) -> None:
    _write_praxis_yaml(tmp_path, domain="create", stage="shape")

    result = transition_stage(tmp_path, "formalize")
    assert result.success

    brief_doc = tmp_path / "docs" / "brief.md"
    assert brief_doc.exists()
    assert "# Creative Brief" in brief_doc.read_text()


def test_create_transition_to_formalize_does_not_overwrite_existing_brief(
    tmp_path: Path,
) -> None:
    _write_praxis_yaml(tmp_path, domain="create", stage="shape")

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir(exist_ok=True)
    brief_doc = docs_dir / "brief.md"
    brief_doc.write_text("EXISTING")

    result = transition_stage(tmp_path, "formalize")
    assert result.success

    assert brief_doc.read_text() == "EXISTING"


def test_write_transition_to_formalize_creates_brief(tmp_path: Path) -> None:
    _write_praxis_yaml(tmp_path, domain="write", stage="shape")

    result = transition_stage(tmp_path, "formalize")
    assert result.success

    brief_doc = tmp_path / "docs" / "brief.md"
    assert brief_doc.exists()
    assert "# Writing Brief" in brief_doc.read_text()


def test_learn_transition_to_formalize_creates_plan(tmp_path: Path) -> None:
    _write_praxis_yaml(tmp_path, domain="learn", stage="shape")

    result = transition_stage(tmp_path, "formalize")
    assert result.success

    plan_doc = tmp_path / "docs" / "plan.md"
    assert plan_doc.exists()
    assert "# Learning Plan" in plan_doc.read_text()
