from pathlib import Path


def test_repository_initialized() -> None:
    """Smoke test to keep CI green while modules are scaffolded."""
    assert Path("README.md").exists()
