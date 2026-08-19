---
id: TASK-0035
title: Backfill Test subtasks onto existing docket tasks
status: Done
created: '2026-08-17'
priority: high
milestone: MS-0002
tags:
  - core
  - tests
acceptance-criteria:
  - 'every open root task has Test: children'
  - 'TASK-0033 and TASK-0034 have Test: children'
  - ensure is idempotent
  - task-list nests the new children
definition-of-done:
  - pytest covers task_ensure_tests
  - CLI --all run on this project
subtasks:
  - TASK-0036
  - TASK-0037
  - TASK-0038
  - TASK-0039
updated: '2026-08-17'
---
Attach Test: children to every open root task plus TASK-0033/0034 using the same generate path as task-create.

**Completion notes:** Backfilled via task-ensure-tests --all plus TASK-0033/0034
