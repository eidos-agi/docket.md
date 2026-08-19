---
id: TASK-0027
title: Add blocked_reason field to ike.md task schema
status: Done
created: '2026-03-21'
priority: medium
dependencies:
  - TASK-0026
acceptance-criteria:
  - blocked_reason field in TaskFrontmatter (optional string)
  - task_edit accepts blocked_reason
  - task_view shows blocked_reason when present
  - tests passing
  - binary rebuilt
subtasks:
  - TASK-0058
  - TASK-0059
  - TASK-0060
  - TASK-0061
  - TASK-0062
updated: '2026-08-17'
---
When a task is blocked, agents have nowhere to record why. The escalation SOP branches on reason type: dependency, info gap, contradiction, resource constraint. Without a structured field, the reason lives in conversation and dies there. Add optional blocked_reason to TaskFrontmatter, task_edit schema, and task_view output. Rebuild and test.

**Completion notes:** blocked_reason already in schema/CLI/view; tests added. 'binary rebuilt' does not apply.
