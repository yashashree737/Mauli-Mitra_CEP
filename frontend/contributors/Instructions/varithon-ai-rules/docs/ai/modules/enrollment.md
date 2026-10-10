# Module: enrollment

Owner: B
Contract file: `src/modules/enrollment/enrollment.contract.js` (LOCKED)
Traces to: U2 — the core action of the whole product

## Purpose

Joining a dindi and the pramukh approval of it. This is the golden-path module.

## Public function list — this list is complete

```
model:   findByDindi(dindiId)
         findByUser(userId)
         create(userId, dindiId)
         updateStatus(enrollmentId, status)
service: enroll(userId, dindiId)
         listForDindi(dindiId, requesterId)
         listForUser(userId, requesterId)
         setStatus(enrollmentId, status, requesterId)
routes:  POST  /api/enrollment
         GET   /api/dindi/:id/enrolled
         GET   /api/users/:id/enrollment
         PATCH /api/enrollment/:id/status
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
