"""Tests for domain specification models and domain creation service."""

import tempfile
from pathlib import Path

import pytest

from praxis.domain.domain_spec import (
    AIConstraint,
    DomainMenuOption,
    DomainSpecification,
)


class TestDomainSpecification:
    """Test DomainSpecification model validation."""

    def test_valid_domain_spec(self):
        """Test creating a valid domain specification."""
        spec = DomainSpecification(
            name="research",
            display_name="Research",
            description="Academic and exploratory investigation",
            formalize_artifact_name="Research Brief",
            formalize_artifact_path="docs/research-brief.md",
            default_privacy="personal",
            ai_permissions={
                "suggest": "allowed",
                "complete": "allowed",
                "generate": "ask",
            },
            subtypes=["academic", "market"],
        )

        assert spec.name == "research"
        assert spec.display_name == "Research"
        assert spec.formalize_artifact_path == "docs/research-brief.md"
        assert len(spec.subtypes) == 2

    def test_domain_name_validation(self):
        """Test domain name must be lowercase alphanumeric with dashes."""
        # Valid names
        DomainSpecification(
            name="valid-name",
            display_name="Valid",
            description="Test",
        )
        DomainSpecification(
            name="valid123",
            display_name="Valid",
            description="Test",
        )

        # Invalid names should raise validation error
        with pytest.raises(Exception):  # Pydantic validation error
            DomainSpecification(
                name="Invalid-Name",  # Uppercase not allowed
                display_name="Invalid",
                description="Test",
            )

        with pytest.raises(Exception):
            DomainSpecification(
                name="123invalid",  # Must start with letter
                display_name="Invalid",
                description="Test",
            )

    def test_artifact_path_validation(self):
        """Test formalize artifact path must be in docs/ and .md."""
        # Valid path
        spec = DomainSpecification(
            name="test",
            display_name="Test",
            description="Test domain",
            formalize_artifact_path="docs/artifact.md",
        )
        assert spec.formalize_artifact_path == "docs/artifact.md"

        # Invalid path (not in docs/)
        with pytest.raises(Exception):
            DomainSpecification(
                name="test",
                display_name="Test",
                description="Test domain",
                formalize_artifact_path="artifact.md",
            )

        # Invalid path (not .md)
        with pytest.raises(Exception):
            DomainSpecification(
                name="test",
                display_name="Test",
                description="Test domain",
                formalize_artifact_path="docs/artifact.txt",
            )

    def test_default_stages(self):
        """Test default allowed stages include all standard stages."""
        spec = DomainSpecification(
            name="test",
            display_name="Test",
            description="Test domain",
        )

        assert "capture" in spec.allowed_stages
        assert "formalize" in spec.allowed_stages
        assert "execute" in spec.allowed_stages
        assert len(spec.allowed_stages) == 9

    def test_ai_constraint_model(self):
        """Test AIConstraint model."""
        constraint = AIConstraint(
            name="citation_required",
            value=True,
            description="Must cite sources",
        )

        assert constraint.name == "citation_required"
        assert constraint.value is True
        assert constraint.description == "Must cite sources"


class TestDomainMenuOption:
    """Test DomainMenuOption model."""

    def test_menu_option_creation(self):
        """Test creating a menu option."""
        option = DomainMenuOption(
            key="research",
            name="research",
            display_name="Research",
            description="Research domain",
            formalize_artifact_name="Research Brief",
            formalize_artifact_path="docs/research-brief.md",
            subtypes=["academic"],
        )

        assert option.key == "research"
        assert option.name == "research"
        assert len(option.subtypes) == 1


class TestDomainCreationService:
    """Test domain creation service functions."""

    def test_list_custom_domains_empty(self):
        """Test listing custom domains when none exist."""
        from praxis.application.domain_creation_service import list_custom_domains

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            domains = list_custom_domains(workspace_path=workspace)
            assert domains == []

    def test_list_custom_domains_with_specs(self):
        """Test listing custom domains from workspace."""
        import yaml

        from praxis.application.domain_creation_service import list_custom_domains

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            domains_dir = workspace / "domains"
            domains_dir.mkdir()

            # Create a domain spec
            spec = DomainSpecification(
                name="research",
                display_name="Research",
                description="Research domain",
            )

            spec_path = domains_dir / "research.yaml"
            with open(spec_path, "w") as f:
                yaml.safe_dump(spec.model_dump(exclude_none=True), f)

            # List domains
            domains = list_custom_domains(workspace_path=workspace)
            assert len(domains) == 1
            assert domains[0].name == "research"

    def test_load_domain_specification(self):
        """Test loading a domain specification by name."""
        import yaml

        from praxis.application.domain_creation_service import (
            load_domain_specification,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            domains_dir = workspace / "domains"
            domains_dir.mkdir()

            # Create a domain spec
            spec = DomainSpecification(
                name="research",
                display_name="Research",
                description="Research domain",
                subtypes=["academic"],
            )

            spec_path = domains_dir / "research.yaml"
            with open(spec_path, "w") as f:
                yaml.safe_dump(spec.model_dump(exclude_none=True), f)

            # Load it
            loaded = load_domain_specification("research", workspace_path=workspace)
            assert loaded is not None
            assert loaded.name == "research"
            assert loaded.display_name == "Research"
            assert "academic" in loaded.subtypes

    def test_load_nonexistent_domain(self):
        """Test loading a domain that doesn't exist."""
        from praxis.application.domain_creation_service import (
            load_domain_specification,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            loaded = load_domain_specification("nonexistent", workspace_path=workspace)
            assert loaded is None

    def test_get_domain_menu_options(self):
        """Test getting predefined menu options."""
        from praxis.application.domain_creation_service import (
            get_domain_menu_options,
        )

        options = get_domain_menu_options()
        assert len(options) > 0

        # Check that research, design, data, and custom are included
        keys = [opt.key for opt in options]
        assert "research" in keys
        assert "design" in keys
        assert "data" in keys
        assert "custom" in keys

        # Check structure of a menu option
        research_opt = next(opt for opt in options if opt.key == "research")
        assert research_opt.name == "research"
        assert research_opt.display_name == "Research"
        assert len(research_opt.subtypes) > 0


class TestDomainSpecificationSerialization:
    """Test YAML serialization of domain specifications."""

    def test_roundtrip_serialization(self):
        """Test that domain spec can be serialized and deserialized."""
        import yaml

        spec = DomainSpecification(
            name="test-domain",
            display_name="Test Domain",
            description="A test domain",
            formalize_artifact_name="Test Brief",
            formalize_artifact_path="docs/test-brief.md",
            default_privacy="personal",
            ai_permissions={"suggest": "allowed", "generate": "ask"},
            subtypes=["type1", "type2"],
            author="test-user",
            version="1.0",
        )

        # Serialize to YAML
        yaml_str = yaml.safe_dump(
            spec.model_dump(exclude_none=True),
            default_flow_style=False,
        )

        # Deserialize back
        data = yaml.safe_load(yaml_str)
        loaded_spec = DomainSpecification(**data)

        assert loaded_spec.name == spec.name
        assert loaded_spec.display_name == spec.display_name
        assert loaded_spec.formalize_artifact_path == spec.formalize_artifact_path
        assert loaded_spec.subtypes == spec.subtypes
        assert loaded_spec.author == spec.author
