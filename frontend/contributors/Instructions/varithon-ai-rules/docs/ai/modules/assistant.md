# Module: assistant

Owner: B
Contract file: `src/modules/assistant/assistant.contract.js` (LOCKED)
Traces to: U1, U2, U3 — answers newcomer questions in plain language

## Purpose

Vari Sahayak. BUILT LAST, only after auth, dindi, enrollment, route and facility all work.
Grounded ONLY in this project's own dindi, route, facility and notice data.
It must never invent a dindi, a facility, or a route stop. If it does not know, it says so.

## Public function list — this list is complete

```
service: answer(question, userId)
         suggestDindi(description, userId)
routes:  POST /api/assistant/ask
         POST /api/assistant/suggest
```

Do not add to this list. If you need another function, write it under
**Contract change requests** below and end your turn.

## Tasks

- [ ] (add task tickets here)

## Contract change requests

_(empty — append: what you need, why, proposed signature)_

## Assumptions

_(empty — append anything you assumed instead of asking)_

## Handoffs

_(append using the format in 60-WORKFLOW.md)_
