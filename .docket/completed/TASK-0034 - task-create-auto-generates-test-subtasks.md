---
id: TASK-0034
title: task-create auto-generates Test subtasks
status: Done
created: '2026-08-17'
priority: high
milestone: MS-0003
tags:
  - core
  - tests
acceptance-criteria:
  - AC items become Test subtasks
  - no AC uses DoD
  - no AC or DoD uses title
  - test children do not spawn tests
  - --no-generate-tests skips
  - config false skips
  - parent.subtasks lists child ids
definition-of-done:
  - pytest covers generate skip recurse config
  - README documents parent and auto tests
updated: '2026-08-17'
subtasks:
  - TASK-0082
  - TASK-0083
  - TASK-0084
  - TASK-0085
  - TASK-0086
  - TASK-0087
  - TASK-0088
---
On create, spawn Test: subtasks from acceptance-criteria, else definition-of-done, else the title. Children have parent set, tag test, and do not recurse. Default on. --no-generate-tests and config task.auto_test_subtasks=false skip.

**Completion notes:** task-create auto Test: subtasks from AC/DoD/title; no recurse; --no-generate-tests and config skip. Proven: tests/test_task.py TestAutoTestSubtasks (76 pytest passed) + CLI proof ~/.cursor/docket-md-auto-test-subtasks.txt
