---
id: TASK-0029
title: Expand visionlog_boot to full session protocol
status: Done
created: '2026-03-21'
priority: medium
dependencies:
  - TASK-0026
  - TASK-0028
acceptance-criteria:
  - visionlog_boot output includes open question count
  - visionlog_boot surfaces goals that have no linked ike tasks (needs decomposition)
  - visionlog_boot includes next-action guidance referencing SOPs
  - tests passing
  - binary rebuilt
subtasks:
  - TASK-0069
  - TASK-0070
  - TASK-0071
  - TASK-0072
  - TASK-0073
updated: '2026-08-17'
---
visionlog_boot currently shows goals and guardrails. It should orient the agent fully: active goals with their ike task counts, open questions, research.md projects in flight, and the decomposition SOP if any goals have no tasks yet. Boot should tell the agent exactly what to call next, not just what the project contains.

**Completion notes:** Won't build. governor research/token-cost-vs-governance-value DECISION.md: do not build full visionlog_boot (token cost). Lightweight boot already exists; open-question count is part of governor.md GOAL-001 if built.
