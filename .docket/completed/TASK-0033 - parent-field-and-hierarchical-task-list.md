---
id: TASK-0033
title: Parent field and hierarchical task-list
status: Done
created: '2026-08-17'
priority: high
milestone: MS-0003
tags:
  - core
  - tests
acceptance-criteria:
  - parent is stored in frontmatter
  - task-list indents children under parent
  - orphans still list
  - task-view shows parent and subtasks
definition-of-done:
  - pytest covers parent field and list nesting
updated: '2026-08-17'
subtasks:
  - TASK-0078
  - TASK-0079
  - TASK-0080
  - TASK-0081
---
Tasks may have parent: TASK-XXXX. task-list nests children under the parent. task-view shows Parent and Subtasks.

**Completion notes:** parent/subtasks frontmatter, nested task-list, task-view Parent+Subtasks. Proven: tests/test_task.py TestParentAndList + ~/.cursor/docket-md-auto-test-subtasks.txt
