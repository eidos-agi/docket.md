---
id: TASK-0011
title: 'Decide: npm publish vs Python rewrite for trilogy distribution'
status: Done
created: '2026-03-21'
priority: high
tags:
  - trilogy
  - distribution
acceptance-criteria:
  - Decision recorded as ADR in visionlog
  - research.md used to earn the decision
  - No packaging work starts until ADR exists
subtasks:
  - TASK-0051
  - TASK-0052
  - TASK-0053
updated: '2026-08-17'
---
All three tools (ike.md, visionlog.md, research.md) are TypeScript. PyPI is Python-only. Decision needed: publish to npm as @eidos-agi/* packages, or rewrite in Python (FastMCP) to match the Eidos ecosystem (resume-resume, claude-session-commons are already on PyPI). Use research.md to earn this decision before acting.

**Completion notes:** Decided: Python / docket-md / PyPI. ADR-001 accepted. npm TypeScript ike.md rejected.
