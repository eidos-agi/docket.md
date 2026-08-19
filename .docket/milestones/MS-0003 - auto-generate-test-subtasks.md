---
id: MS-0003
title: Auto-generate test subtasks
status: closed
created: '2026-08-17'
---
task-create automatically generates test tasks as children of the created task. Each acceptance criterion (else DoD, else the title) becomes a Test: subtask with parent set. Config task.auto_test_subtasks defaults on. --no-generate-tests skips. Test subtasks do not spawn further tests.

**Closed:** parent + auto Test: subtasks shipped. pytest 76 passed. CLI proof ~/.cursor/docket-md-auto-test-subtasks.txt
