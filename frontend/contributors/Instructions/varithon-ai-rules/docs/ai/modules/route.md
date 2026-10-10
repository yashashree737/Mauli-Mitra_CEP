# Module: route

Owner: B
Contract file: `src/modules/route/route.contract.js` (LOCKED)
Traces to: U3 — removes the fear of the distance and the villages

## Purpose

Day-wise route stops for a dindi: day number, halt village, km, coordinates.

## Public function list — this list is complete

```
model:   findByDindi(dindiId)
         create(stopData)
service: getJourney(dindiId, requesterId)
         addStop(stopData, requesterId)
routes:  GET  /api/dindi/:id/route
         POST /api/dindi/:id/route
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
