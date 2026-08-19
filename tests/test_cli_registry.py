"""TASK-0101 — CLI project registration must survive across processes.

Covers the three acceptance criteria:
1. task-create (and siblings) from outside a registered project errors LOUDLY
   (nonzero exit, clear message) — never a silent no-op with exit 0.
2. project-init / project-set / boot_from_cwd persist {guid: path} to the CLI
   registry file; resolve_project falls back to it from a fresh process,
   re-validating docket.json existence + id match. Stale entries are rejected.
3. Error messages distinguish the MCP-session case from the CLI-process case.
"""

import json
import os
import shutil
import subprocess
import sys

import pytest

from docket_md import config as cfg

# Runs the real console entry point (fresh process = fresh _guid_to_path).
CLI_SCRIPT = (
    "import sys; from docket_md.cli import main; "
    "sys.argv = ['docket-md'] + sys.argv[1:]; main()"
)


def run_cli(args, cwd, registry_path):
    env = dict(os.environ)
    env[cfg.CLI_REGISTRY_ENV] = str(registry_path)
    return subprocess.run(
        [sys.executable, "-c", CLI_SCRIPT, *args],
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )


@pytest.fixture()
def registry(tmp_path):
    return tmp_path / "cli-registry.json"


@pytest.fixture()
def elsewhere(tmp_path):
    d = tmp_path / "elsewhere"
    d.mkdir()
    return d


def _init_project(tmp_path, registry, elsewhere, name="regproj"):
    proj = tmp_path / name
    proj.mkdir()
    result = run_cli(["project-init", str(proj), "--name", name], elsewhere, registry)
    assert result.returncode == 0, result.stderr
    guid = json.loads((proj / ".docket" / "docket.json").read_text())["id"]
    return proj, guid


class TestLoudFailure:
    def test_task_create_unknown_guid_errors_loudly(
        self, tmp_path, registry, elsewhere
    ):
        """The old silent no-op (exit 0, empty output) must be impossible."""
        result = run_cli(
            [
                "task-create",
                "--project-id",
                "00000000-0000-0000-0000-000000000000",
                "--title",
                "should fail loudly",
            ],
            elsewhere,
            registry,
        )
        assert result.returncode != 0
        combined = result.stdout + result.stderr
        assert combined.strip(), "must never fail silently"
        assert "Unknown project_id" in combined
        # CLI-shaped remedy, not MCP-shaped (AC3).
        assert "docket-md project-set" in combined
        assert "MCP session" not in combined

    def test_task_create_missing_project_id_is_cli_shaped(
        self, tmp_path, registry, elsewhere
    ):
        # Typer enforces --project-id, so the missing-option error is loud too.
        result = run_cli(["task-create", "--title", "x"], elsewhere, registry)
        assert result.returncode != 0
        assert (result.stdout + result.stderr).strip()


class TestRegistryFallback:
    def test_project_init_persists_and_resolves_from_another_cwd(
        self, tmp_path, registry, elsewhere
    ):
        proj, guid = _init_project(tmp_path, registry, elsewhere)
        # Registration persisted to the registry file.
        assert json.loads(registry.read_text())[guid] == str(proj)
        # A brand-new process from an unrelated cwd resolves the guid.
        result = run_cli(
            ["task-create", "--project-id", guid, "--title", "born elsewhere"],
            elsewhere,
            registry,
        )
        assert result.returncode == 0, result.stderr
        assert "Created" in result.stdout
        tasks = os.listdir(proj / ".docket" / "tasks")
        assert any("born-elsewhere" in f for f in tasks)

    def test_project_set_persists_across_invocations(
        self, tmp_path, registry, elsewhere
    ):
        proj, guid = _init_project(tmp_path, registry, elsewhere)
        registry.unlink()  # forget the init-time registration
        result = run_cli(["project-set", str(proj)], elsewhere, registry)
        assert result.returncode == 0, result.stderr
        result = run_cli(
            ["task-list", "--project-id", guid], elsewhere, registry
        )
        assert result.returncode == 0, result.stderr

    def test_boot_from_cwd_persists_registration(
        self, tmp_path, registry, elsewhere
    ):
        proj, guid = _init_project(tmp_path, registry, elsewhere)
        registry.unlink()
        # Any command run from inside the project re-registers it on boot...
        result = run_cli(["project-list"], proj, registry)
        assert result.returncode == 0, result.stderr
        assert json.loads(registry.read_text())[guid] == str(proj)
        # ...making it resolvable from elsewhere afterwards.
        result = run_cli(["task-list", "--project-id", guid], elsewhere, registry)
        assert result.returncode == 0, result.stderr


class TestStaleRegistry:
    def test_project_moved_or_deleted_is_rejected_clearly(
        self, tmp_path, registry, elsewhere
    ):
        proj, guid = _init_project(tmp_path, registry, elsewhere)
        shutil.rmtree(proj)
        result = run_cli(
            ["task-create", "--project-id", guid, "--title", "into the void"],
            elsewhere,
            registry,
        )
        assert result.returncode != 0
        combined = result.stdout + result.stderr
        assert "Stale CLI registry entry" in combined
        assert "moved or deleted" in combined

    def test_id_mismatch_is_rejected_clearly(self, tmp_path, registry, elsewhere):
        proj, guid = _init_project(tmp_path, registry, elsewhere)
        # The project on disk got a different id (re-init, restore, etc.).
        cfg_path = proj / ".docket" / "docket.json"
        data = json.loads(cfg_path.read_text())
        data["id"] = "11111111-1111-1111-1111-111111111111"
        cfg_path.write_text(json.dumps(data))
        result = run_cli(
            ["task-list", "--project-id", guid], elsewhere, registry
        )
        assert result.returncode != 0
        combined = result.stdout + result.stderr
        assert "Stale CLI registry entry" in combined
        assert "now has id" in combined


class TestMcpBehaviorUnchanged:
    def test_mcp_runtime_does_not_touch_registry_and_keeps_mcp_message(
        self, tmp_path, monkeypatch
    ):
        registry = tmp_path / "cli-registry.json"
        monkeypatch.setenv(cfg.CLI_REGISTRY_ENV, str(registry))
        monkeypatch.setattr(cfg, "RUNTIME", "mcp")
        proj = tmp_path / "mcpproj"
        proj.mkdir()
        cfg.init_project(str(proj), "mcpproj")
        cfg.register_project(str(proj))
        # No on-disk write in MCP runtime.
        assert not registry.exists()
        # Unknown guid gets the MCP-session-shaped message, no registry fallback.
        # (Write a registry entry to prove MCP ignores it.)
        other = tmp_path / "otherproj"
        other.mkdir()
        other_cfg = cfg.init_project(str(other), "otherproj")
        registry.write_text(json.dumps({other_cfg.id: str(other)}))
        cfg._guid_to_path.pop(other_cfg.id, None)
        with pytest.raises(ValueError, match="MCP session"):
            cfg.resolve_project(other_cfg.id)
