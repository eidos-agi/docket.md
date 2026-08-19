---
id: MS-0004
title: Call shipr CLI on milestone-close
status: closed
created: '2026-08-17'
---
When a milestone is closed, docket-md invokes the shipr CLI (`shipr attempt --status shipped`) against the project root. Shipr records the release ledger; it does not deploy. Skip with --no-shipr or config shipr.enabled=false. Missing shipr on PATH does not fail the close.

**Closed:** pytest green; shipr attempt on close
