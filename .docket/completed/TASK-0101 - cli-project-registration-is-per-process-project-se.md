---
id: TASK-0101
title: CLI project registration is per-process — project-set from another cwd succeeds then vanishes
status: Done
created: '2026-08-19'
priority: Medium
tags:
  - bug
  - cli
acceptance-criteria:
  - task-create from outside a project errors loudly, never silent no-op exit 0
  - either project-set persists across invocations or its output says it cannot
  - error message distinguishes MCP session vs CLI process
updated: '2026-08-19'
---
2026-08-19: from a different working directory, 'docket-md project-set <path>' prints 'Project registered' but the very next docket-md invocation errors 'Unknown project_id... Call project_set' — registration lives in the in-memory _guid_to_path dict (config.py) and each CLI invocation is a fresh process; only cli/_app.py boot_from_cwd() works, silently requiring cwd inside the project. Two fixes possible: (a) honest error — project-set warns it cannot persist across processes and suggests cd; (b) real fix — persist registrations to a session file (~/.docket/session-registry.json keyed by tty/session) so the MCP-shaped advice in the error message actually works for CLI users. Also: task-create from wrong cwd fails SILENTLY (empty output, no task, exit 0) — that is the worst variant; it must error loudly.

**Completion notes:** Fixed in 9565de8: CLI runtime persists guid->path to ~/.docket-md/cli-registry.json (atomic, validated fallback in resolve_project); errors are loud and CLI-shaped vs MCP-shaped; covered by tests/test_cli_registry.py (8 tests, full suite 100 passed).
