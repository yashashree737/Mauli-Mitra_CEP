# 30-CONVENTIONS

Two runtimes, two casing worlds. The boundary is `frontend/src/lib/api.js`.

## Backend — Python / FastAPI

| Thing | Convention | Example |
|---|---|---|
| variables, functions | snake_case | `enrolled_warkaris`, `find_by_dindi` |
| classes, Pydantic schemas, SQLModel tables | PascalCase | `EnrolledUser`, `DindiSummary` |
| module files | lowercase layer name | `service.py`, `repository.py` |
| constants and enum members | SCREAMING_SNAKE | `EnrollmentStatus.PENDING` |
| db columns | snake_case, matches the model exactly | `start_village` |
| booleans | `is_` / `has_` / `can_` prefix | `is_verified` |
| API paths | lowercase, plural-free, kebab if needed | `/api/dindi/{dindi_id}/enrolled` |
| query params | snake_case | `?village=&start_date=` |

Verb vocabulary — use only these, do not invent more:
`find` `find_by_id` `find_by_<x>` `list` `create` `update` `update_status` `remove`

Service functions read as intent: `enroll`, `set_status`, `verify_dindi`, `get_journey`.
Never `get_` + `fetch_` + `load_` for the same thing. That is the sprawl this file exists to stop.

Type hints on every function signature. Return types included. No bare `def f(x):`.

## Frontend — JavaScript / Next.js

| Thing | Convention | Example |
|---|---|---|
| variables, functions | camelCase | `enrolledWarkaris`, `findByDindi` |
| components | PascalCase | `DindiCard` |
| component files | PascalCase.jsx | `DindiCard.jsx` |
| constants | SCREAMING_SNAKE | `ENROLLMENT_STATUS` |
| booleans | is / has / can prefix | `isVerified` |

## The one rule that connects them

The wire is **snake_case**. `api.js` camelizes responses and decamelizes request bodies.
A component sees `dindi.startVillage`. The backend sees `start_village`. Neither knows the other exists.

## File layout per backend module

    backend/app/modules/enrollment/
      contract.py      LOCKED  Pydantic schemas + the function list
      repository.py    OPEN    db calls only
      service.py       OPEN    logic and permission checks
      router.py        OPEN    routes only
      __init__.py      OPEN    exports the router

## Every file declares its function list at the top

    # backend/app/modules/enrollment/repository.py
    #
    # PUBLIC FUNCTIONS (this list is complete - do not add without approval)
    # find_by_dindi(session, dindi_id)
    # find_by_user(session, user_id)
    # create(session, user_id, dindi_id)
    # update_status(session, enrollment_id, status)

## Nothing private

Every function in a module file appears in that list.
No `_format_user` helpers hiding at the bottom.
Never write a helper called from only one place — inline it.

## Frontend rules

- Mobile first. Write the 380px layout, then add breakpoints upward.
- Tailwind utility classes only. Tokens in `tailwind.config.js`.
- One component per file, under 150 lines. Split if longer.
- Every list has a loading state, an empty state and an error state. All three.
- Every page renders something when the API is down.

## Content

All user-facing strings live in `content/`. Marathi and English side by side. UTF-8, no escaping.

## Linting

Backend: `ruff` (or `black` + `flake8`) before ending your turn.
Frontend: `eslint` + `prettier` before ending your turn.
Do not edit the lint config to make it pass.
