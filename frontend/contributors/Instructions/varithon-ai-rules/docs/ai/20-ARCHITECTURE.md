# 20-ARCHITECTURE

## Runtime split

    frontend/   Next.js, JavaScript, deployed to Vercel
    backend/    FastAPI, Python 3.11+, SQLModel, Postgres

They communicate over HTTP/JSON only. No shared code, no shared types.
`NEXT_PUBLIC_API_URL` is the only thing the frontend knows about the backend.

## Three layers, no more (backend)

    router      -> validates with a Pydantic schema, resolves the current user,
                   calls ONE service function, returns a response model
    service     -> the actual logic, enforces permissions, calls the repository
    repository  -> talks to the database, nothing else

A router never touches the database. A repository never checks permissions.
If code does not fit one of these three layers, it does not get written.

Permission checks live in the **service**, not the router and not the repository.
Auth (who are you) is a router dependency. Authorization (may you) is service work.

## Backend module layout

    backend/app/
      main.py                     app factory, CORS, router registration
      core/
        config.py                 settings from env
        security.py               JWT create/verify, password/otp
        deps.py                   get_db, get_current_user, require_role
        errors.py                 the error shape, exception handlers
      constants/
        roles.py                  Role enum
        enrollment.py             EnrollmentStatus enum
        facility.py               FacilityType enum
      models/                     SQLModel tables, one file per model
      modules/
        auth/         contract.py  router.py  service.py  repository.py
        users/        same four
        dindi/        same four
        enrollment/   same four
        route/        same four
        facility/     same four
        safety/       same four
        assistant/    contract.py  router.py  service.py   (no repository — reads via other services)
      seed/
        load.py                    loads seed/*.json into the DB

`notice/` is CUT. Notices are static content rendered by the frontend from seed data.

## Frontend layout

    frontend/
      src/app/                    pages, one folder per route
      src/components/             shared components
      src/lib/api.js              THE ONLY file that calls the backend
      src/lib/case.js             snake_case <-> camelCase conversion
      content/                    all user-facing strings, Marathi + English
      tailwind.config.js          design tokens

## The case boundary — the rule that prevents the worst bug of the weekend

**The wire format is snake_case.** FastAPI emits snake_case and accepts snake_case.

The frontend converts **once**, inside `src/lib/api.js`, using `src/lib/case.js`.
Every response is converted snake_case -> camelCase on the way in.
Every request body is converted camelCase -> snake_case on the way out.

    No component ever reads `data.start_village`.
    No backend code ever emits `startVillage`.
    No `response_model_by_alias`, no camelCase aliases in Pydantic. Do not add them.

If you find yourself writing a case conversion outside `src/lib/case.js`, STOP.

## Data models

    User          id, name, phone, village, language, is_first_timer, role, created_at
    Dindi         id, name, start_village, route, language, capacity,
                  is_verified, pramukh_id ---> User.id
    EnrolledUser  id, user_id ---> User.id, dindi_id ---> Dindi.id, enrolled_at, status
    RouteStop     id, dindi_id ---> Dindi.id, day_number, village_name, km, lat, lng
    Facility      id, type, name, lat, lng, village_name, contact, timing

Enums — import from `app/constants/`, never type the string literal:

    Role                user | pramukh | admin
    EnrollmentStatus    pending | active | left
    FacilityType        medical | water | toilet | food | rest | police

Those arrows are the only legal joins.
`Notice` is not a table. It is seed content.

## Permission grid

| Role | User | EnrolledUser | Dindi | RouteStop | Facility |
|---|---|---|---|---|---|
| Guest | — | — | read verified | read | read |
| User | own only | own only | read verified | read | read |
| Pramukh | read in dindi | full in dindi | edit own dindi | edit own dindi | read |
| Admin | full | full | full + verify | full | full |

No cell is ambiguous. Do not invent permission logic beyond this table.
If a case is not covered here, STOP and log it in the module doc.

## Canonical request flow — every endpoint follows this shape

    GET /api/dindi?village=&language=&route=
      -> router: query params parsed into DindiListQuery (Pydantic)
      -> router: current_user = Depends(get_current_user_optional)
      -> service.list_dindis(query, current_user)
           guests and users -> is_verified == True only
           admin            -> all
      -> repository.list(filters)
      -> returns list[DindiSummary]
      -> not permitted -> raise Forbidden

Frontend side:

    src/lib/api.js  ->  fetch  ->  camelize  ->  page component

## Error shape — identical on every failure

    { "error": { "code": "NOT_FOUND", "message": "Dindi not found" } }

Codes: `VALIDATION_ERROR` `UNAUTHORIZED` `FORBIDDEN` `NOT_FOUND` `CONFLICT` `SERVER_ERROR`

Raise the app's own exception classes from `core/errors.py`.
Never return a raw traceback, a SQLAlchemy error, or FastAPI's default 422 body.
A single exception handler maps everything into the shape above.

## Import direction

- A module may import `app/core/`, `app/constants/`, `app/models/` freely.
- A module may NOT import another module's `repository.py`.
- Cross-module reads go through the owning module's `service.py`.
- `assistant/` reads through other services only. It gets no direct DB access.
- Never add a package without an ADR in `decisions/`.

## Deployment

    frontend  -> Vercel
    backend   -> single container/host, Postgres attached
    CORS      -> configured in main.py from an env allowlist, not "*"

Both deploy independently. **A broken backend must not break the frontend build.**
Every page renders something — a loading, empty, or error state — when the API is down.
