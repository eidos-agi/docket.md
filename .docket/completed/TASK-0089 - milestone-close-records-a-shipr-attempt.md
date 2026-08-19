---
id: TASK-0089
title: milestone-close records a shipr attempt
status: Done
created: '2026-08-17'
priority: high
milestone: MS-0004
tags:
  - core
  - shipr
acceptance-criteria:
  - close still writes status=closed first
  - shipr attempt is invoked with project root and shipped status
  - goal includes milestone id and title
  - --no-shipr skips the CLI
  - config shipr.enabled false skips
  - missing shipr on PATH skips without failing close
  - close output mentions shipr result
definition-of-done:
  - pytest covers invoke skip missing-binary
  - README documents the hook
subtasks:
  - TASK-0090
  - TASK-0091
  - TASK-0092
  - TASK-0093
  - TASK-0094
  - TASK-0095
  - TASK-0096
updated: '2026-08-17'
---
After writing status=closed, run shipr attempt --project <root> --goal 'Close MS-XXXX: title' --status shipped --proof 'docket-md milestone-close MS-XXXX' --json. Default on. --no-shipr and config shipr.enabled=false skip. Missing binary skips without failing the close.

**Completion notes:** Proven by tests/test_shipr_hook.py
