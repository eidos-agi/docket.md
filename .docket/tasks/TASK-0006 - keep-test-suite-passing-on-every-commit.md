---
id: TASK-0006
title: Keep test suite passing on every commit
status: To Do
created: '2026-03-21'
priority: high
milestone: MS-0002
tags:
  - evergreen
  - regression
definition-of-done:
  - pytest passes (or more) after every change
  - No skipped or commented-out tests
  - New behavior = new test before merging
subtasks:
  - TASK-0040
  - TASK-0041
  - TASK-0042
updated: '2026-08-17'
---
npm test must pass before any push. If a test breaks, fix it before merging. This is a standing commitment — not a one-time task.

DoD updated 2026-08-17: npm test 49/49 was the TypeScript suite. Python docket-md uses pytest.
