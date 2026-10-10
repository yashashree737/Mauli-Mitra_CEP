# Module: safety

Owner: B
Contract file: `src/modules/safety/safety.contract.js` (LOCKED)
Traces to: U3 — the fear removal feature

## Purpose

SOS numbers and a shareable live-location link for family. No tracking stored beyond the share.

## Public function list — this list is complete

```
model:   createShare(userId, expiresAt)
         findShare(shareToken)
service: getEmergencyContacts(userId)
         startLocationShare(userId)
         resolveShare(shareToken)
routes:  GET  /api/safety/contacts
         POST /api/safety/share
         GET  /api/safety/share/:token
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
