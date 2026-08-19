---
id: TASK-0028
title: Add open questions construct to visionlog
status: Done
created: '2026-03-21'
priority: medium
dependencies:
  - TASK-0026
acceptance-criteria:
  - question_create tool exists
  - question_list tool exists
  - question_resolve tool exists (links to ADR or research ID)
  - visionlog_boot shows open question count
  - tests passing
  - binary rebuilt
subtasks:
  - TASK-0063
  - TASK-0064
  - TASK-0065
  - TASK-0066
  - TASK-0067
  - TASK-0068
updated: '2026-08-17'
---
Named unknowns have no home in the trilogy. An open question is not a goal, not an ADR, not a guardrail — but agents need to see them during sessions. Add a question_create / question_list / question_resolve set of tools to visionlog. A question has: title, body, date, status (open/resolved), and optional resolution (ADR-xxx or research project ID that answered it). visionlog_boot should surface open questions count.

**Completion notes:** Not implemented in docket-md. Relocated to governor.md GOAL-001 (open questions construct). docket.md is execution; named unknowns belong in governor.
