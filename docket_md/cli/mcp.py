"""``docket-md mcp serve`` — boots the razor-thin MCP server."""

from __future__ import annotations

import typer

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command("serve")
def cmd_serve() -> None:
    """Run the MCP server over stdio (entry point for MCP hosts)."""
    from .. import config as _cfg
    from ..mcp_server import run

    # The root callback marks every docket-md process as RUNTIME="cli", but this
    # command becomes a long-lived MCP server — restore in-memory-only behavior.
    _cfg.RUNTIME = "mcp"
    run()
