"""Tests for application settings."""

from concert_planner.config.settings import (
    LANGSMITH_PROJECT,
    LANGSMITH_TRACING,
    PROJECT_ROOT,
)


def test_project_root_exists():
    """The project root should point to an existing directory."""
    assert PROJECT_ROOT.exists()
    assert (PROJECT_ROOT / "pyproject.toml").exists()


def test_langsmith_defaults():
    """LangSmith settings should use the configured defaults."""
    assert LANGSMITH_PROJECT == "encore-ai"
    assert LANGSMITH_TRACING is False
