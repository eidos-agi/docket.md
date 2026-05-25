"""CLI session boot — auto-register projects from filesystem before any tool call.

The MCP server kept a long-lived in-memory ``project_id → path`` map; a
fresh CLI subprocess does not. ``boot_from_cwd()`` walks up from CWD,
finds any directory with ``.docket/docket.json`` OR ``.eidos/docket/docket.json``,
and registers it.

When called from inside an eidos (``<eidos_home>/.eidos/docket/`` exists),
docket-md respects the eidos's storage layout. When called standalone
(``<repo>/.docket/`` exists), it uses the legacy layout. This is the
"eidos-aware but eidos-not-required" property per THE-EIDOS doctrine.
"""

from __future__ import annotations

from pathlib import Path

from .. import config as _cfg
from ..config import register_project


def _walk_up_for_docket(start: Path) -> Path | None:
    """Walk up looking for a docket project.

    Resolution order at each level:

    1. ``<level>/.eidos/docket/docket.json`` — eidos-aware (DOCKET_DIR
       is monkey-patched to ``.eidos/docket`` by eidos-cli's root callback
       before this fires).
    2. ``<level>/.docket/docket.json`` — legacy standalone layout.
    """
    cur = start.resolve()
    while True:
        # Honor whatever DOCKET_DIR is set to (eidos-cli may have patched
        # it to .eidos/docket; otherwise it's the legacy .docket).
        if (cur / _cfg.DOCKET_DIR / "docket.json").is_file():
            return cur
        # Also explicitly check the eidos-aware path even if DOCKET_DIR
        # hasn't been patched — so standalone docket-md inside an eidos
        # finds the right project too.
        if (cur / ".eidos" / "docket" / "docket.json").is_file():
            _cfg.DOCKET_DIR = ".eidos/docket"
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent


def boot_from_cwd(path: str | None = None) -> None:
    """Register any docket project rooted at or above CWD.

    Safe to call repeatedly. Silently no-ops if no project is found.
    """
    start = Path(path).resolve() if path else Path.cwd()
    root = _walk_up_for_docket(start)
    if root is None:
        return
    try:
        register_project(str(root))
    except Exception:
        return
