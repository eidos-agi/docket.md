"""Project configuration and GUID registry."""

import json
import os
import tempfile
import uuid
from dataclasses import dataclass
from datetime import date

DOCKET_DIR = ".docket"
CONFIG_FILENAME = "docket.json"

# Which runtime drives this process: "mcp" (long-lived server, in-memory
# registration is enough) or "cli" (fresh process per invocation, needs the
# on-disk registry). cli/_app.py flips this to "cli" before any command runs.
RUNTIME = "mcp"

# Env var that overrides the CLI registry file location (used by tests).
CLI_REGISTRY_ENV = "DOCKET_MD_CLI_REGISTRY"

DIRECTORIES = {
    "TASKS": "tasks",
    "COMPLETED": "completed",
    "ARCHIVE": "archive",
    "MILESTONES": "milestones",
    "DOCUMENTS": "documents",
    "GRAPH": "graph",
    "PLANS": "plans",
}

# In-memory GUID → path registry. Per-process; the CLI runtime additionally
# persists registrations to a small on-disk registry so a fresh process can
# resolve a GUID registered by an earlier invocation.
_guid_to_path: dict[str, str] = {}


def cli_registry_path() -> str:
    """Location of the cross-process CLI registry file."""
    override = os.environ.get(CLI_REGISTRY_ENV)
    if override:
        return override
    return os.path.join(os.path.expanduser("~"), ".docket-md", "cli-registry.json")


def _load_cli_registry() -> dict[str, str]:
    try:
        with open(cli_registry_path()) as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(k): str(v) for k, v in data.items()}


def _persist_registration(guid: str, abs_path: str) -> None:
    """Best-effort atomic upsert of {guid: abs_path} into the CLI registry."""
    try:
        registry = _load_cli_registry()
        if registry.get(guid) == abs_path:
            return
        registry[guid] = abs_path
        reg_path = cli_registry_path()
        reg_dir = os.path.dirname(reg_path) or "."
        os.makedirs(reg_dir, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=reg_dir, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(registry, f, indent=2)
                f.write("\n")
            os.replace(tmp_path, reg_path)
        except BaseException:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise
    except Exception:
        # The registry is a convenience; never fail the command over it.
        return


@dataclass
class DocketConfig:
    id: str
    version: str
    project: str
    created: str
    docket_path: str


def load_config(dir_path: str) -> DocketConfig | None:
    config_path = os.path.join(dir_path, DOCKET_DIR, CONFIG_FILENAME)
    if not os.path.exists(config_path):
        return None
    try:
        with open(config_path) as f:
            data = json.load(f)
        return DocketConfig(**data)
    except Exception:
        return None


def save_config(dir_path: str, config: DocketConfig) -> None:
    docket_dir = os.path.join(dir_path, DOCKET_DIR)
    os.makedirs(docket_dir, exist_ok=True)
    with open(os.path.join(docket_dir, CONFIG_FILENAME), "w") as f:
        json.dump(
            {
                "id": config.id,
                "version": config.version,
                "project": config.project,
                "created": config.created,
                "docket_path": config.docket_path,
            },
            f,
            indent=2,
        )
        f.write("\n")


def init_project(target_dir: str, project_name: str | None = None) -> DocketConfig:
    docket_dir = os.path.join(target_dir, DOCKET_DIR)
    for d in DIRECTORIES.values():
        os.makedirs(os.path.join(docket_dir, d), exist_ok=True)

    existing = load_config(target_dir)
    if existing:
        return existing

    config = DocketConfig(
        id=str(uuid.uuid4()),
        version="0.1.0",
        project=project_name or os.path.basename(os.path.abspath(target_dir)),
        created=date.today().isoformat(),
        docket_path=DOCKET_DIR,
    )
    save_config(target_dir, config)
    return config


def register_project(project_path: str) -> dict[str, str]:
    abs_path = os.path.abspath(project_path)
    config = load_config(abs_path)
    if not config:
        raise ValueError(
            f"No docket.json at {abs_path}. Call project_init first to initialize docket.md in this directory."
        )
    _guid_to_path[config.id] = abs_path
    if RUNTIME == "cli":
        _persist_registration(config.id, abs_path)
    return {"id": config.id, "project": config.project}


def _resolve_from_cli_registry(project_id: str) -> str:
    """Fallback for fresh CLI processes: resolve via the on-disk registry.

    Re-validates the entry (docket.json still there, id still matches)
    before trusting it. Raises ValueError with a CLI-shaped message.
    """
    project_path = _load_cli_registry().get(project_id)
    if not project_path:
        raise ValueError(
            f"Unknown project_id '{project_id}'. It is not registered in this CLI "
            f"process and not found in the CLI registry ({cli_registry_path()}). "
            "Run `docket-md project-set <project-path>` once to register it "
            "(registration persists across CLI invocations), or run docket-md from "
            "inside the project directory. The project_id is the 'id' field in the "
            "project's docket.json."
        )
    config = load_config(project_path)
    if not config:
        raise ValueError(
            f"Stale CLI registry entry for project_id '{project_id}': no readable "
            f"docket.json under {project_path} (project moved or deleted?). "
            "Re-register with `docket-md project-set <new-path>`, or remove the "
            f"entry from {cli_registry_path()}."
        )
    if config.id != project_id:
        raise ValueError(
            f"Stale CLI registry entry for project_id '{project_id}': the project at "
            f"{project_path} now has id '{config.id}'. Re-register with "
            f"`docket-md project-set {project_path}` to pick up the current id, or "
            f"remove the entry from {cli_registry_path()}."
        )
    _guid_to_path[project_id] = project_path
    return project_path


def resolve_project(project_id: object) -> str:
    if not project_id or not isinstance(project_id, str):
        if RUNTIME == "cli":
            raise ValueError(
                "Missing required parameter: --project-id. "
                "Run `docket-md project-set <project-path>` to register the project "
                "and print its GUID, or `docket-md project-init <path>` to create a "
                "new docket.md project."
            )
        raise ValueError(
            "Missing required parameter: project_id. "
            "Call project_set with the project path to register it and get its GUID. "
            "Or call project_init to create a new docket.md project."
        )
    project_path = _guid_to_path.get(project_id)
    if project_path:
        return project_path
    if RUNTIME == "cli":
        return _resolve_from_cli_registry(project_id)
    raise ValueError(
        f"Unknown project_id '{project_id}'. This project hasn't been registered "
        "in this MCP session. Call project_set with the project path to register "
        "it. The project_id is the 'id' field in the project's docket.json."
    )


def list_registered() -> list[dict[str, str]]:
    return [{"id": id, "path": p} for id, p in _guid_to_path.items()]
