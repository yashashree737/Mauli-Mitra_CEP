# Module: dindi

Owner: B
Contract file: `src/modules/dindi/dindi.contract.js` (LOCKED)
Traces to: U1, U2 — shows the Wari is organised, and which dindi will take you

## Purpose

Dindi records and admin verification. Guests and users see verified dindis only.

## Public function list — this list is complete

```
model:   findById(dindiId)
         list(filters)
         update(dindiId, patch)
service: listDindis(filters, requesterRole)
         getDindi(dindiId, requesterRole)
         verifyDindi(dindiId, adminId)
routes:  GET   /api/dindi
         GET   /api/dindi/:id
         PATCH /api/dindi/:id/verify
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
