# Module: facility

Owner: B
Contract file: `src/modules/facility/facility.contract.js` (LOCKED)
Traces to: U3 — removes the fear about safety and basic needs on the route

## Purpose

Medical, water, toilet, food, rest and police facilities along the route, plus nearest lookup.

## Public function list — this list is complete

```
model:   list(filters)
         findById(facilityId)
service: listFacilities(filters)
         findNearest(lat, lng, type)
routes:  GET /api/facility
         GET /api/facility/nearest
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
