# 40-EDIT-POLICY — the safety file

Highest precedence after the task ticket. Style rules never override this file.

## LOCKED vs OPEN

LOCKED paths:

    backend/app/modules/*/contract.py     Pydantic request/response schemas + function list
    backend/app/constants/*.py            Role, EnrollmentStatus, FacilityType
    backend/app/models/*.py               SQLModel tables (locked at CONTRACTS LOCKED)
    backend/app/core/errors.py            the error shape
    frontend/src/lib/api.js               the fetch boundary
    frontend/src/lib/case.js              the case conversion
    docs/ai/**                            every rule file

Everything else is OPEN, subject to `50-OWNERSHIP.md`.

When one file is forced on you — a React component, a config, a migration — use markers:

    # == LOCKED =====================================
    # id: enrollment.contract.v1   owner: architect
    # Do not edit. Change requires an UNLOCK token in the commit message.
    class EnrollmentStatus(str, Enum):
        PENDING = "pending"
        ACTIVE = "active"
        LEFT = "left"
    # == END LOCKED =================================

    # == OPEN =======================================
    # id: enrollment.impl   owner: agent-b
    # Editable. Must satisfy the LOCKED contract above.
    async def create(session, user_id: str, dindi_id: str) -> EnrolledUser:
        ...
    # == END OPEN ===================================

JavaScript files use `// ==` instead of `# ==`. Everything else is identical.

## The rules

    You may modify only bytes between OPEN and END OPEN, in a file
    whose owner in 50-OWNERSHIP.md is you.

    Never edit a LOCKED block or a LOCKED file. This includes whitespace,
    import order, comment rewording, and formatting. Byte-identical or it
    is a violation.

    Never delete, move, or reword a marker line.
    Never rewrite a whole file when asked to change part of it.
    Never create a file outside your owned paths.

    Do not create new functions. Implement the ones already listed in the
    module contract. If you need one that is not listed: STOP and request it
    in modules/<module>.md.

    Never write a helper called from only one place. Inline it.
    Maximum three layers: router -> service -> repository. Nothing else.

    If your task needs a LOCKED change: STOP, append the request to
    modules/<module>.md with the reason and the proposed signature, end turn.
    Do not implement around it.
    Do not duplicate the locked schema under a new name.

    When creating a NEW module file, emit both sections. Pydantic schemas,
    enums and the function list go in LOCKED. All bodies go in OPEN.

## Python-specific bans

- **No `response_model_by_alias`, no camelCase aliases in Pydantic.** The wire is snake_case.
- No `dict` or `Any` as a response model. Every endpoint returns a declared Pydantic model.
- No raw SQL string interpolation. SQLModel/SQLAlchemy expressions only.
- No `except Exception: pass`. Catch what you handle, raise the app's error classes.
- No business logic in `models/`. Tables are data, not behaviour.
- No `print()`. Use the configured logger.
- No sync DB calls inside an async route.

## JavaScript-specific bans

- No `fetch()` outside `src/lib/api.js`.
- No case conversion outside `src/lib/case.js`.
- No hardcoded API URL. Read `NEXT_PUBLIC_API_URL`.
- No hardcoded hex colour. Tokens live in `tailwind.config.js`.
- No user-facing string hardcoded in a component. It goes in `content/`.
- No `localStorage` for anything that belongs on the server.

## Scope bans — these cost hours the team does not have

- No new package in either runtime without an ADR in `decisions/`.
- **No vector DB, embeddings, LangChain, or RAG framework.** See 10-CONTEXT.
- No Alembic migration chain. The schema is created from SQLModel at startup.
- No test framework setup. D tests by running the written test script.
- No rebuilding anything in the CUT table in `10-CONTEXT.md`.
- No refactor bundled into feature work. One ticket, one concern.

## Escalation path when blocked

1. Append to `docs/ai/modules/<module>.md` under **Contract change requests**:
   what you need, why, and the exact proposed signature.
2. Append anything you assumed to the **Assumptions** section of the same file.
3. End your turn. Do not proceed on the assumption.
4. A human — not an agent — resolves it and edits the LOCKED file.

## Hard bans

- No commit directly to `main`.
- No secrets, keys, tokens or real phone numbers in the repo. `.env` only, and `.env` is gitignored.
- No real personal data in seed files. Invented names only.
- No change to the golden-path pages by anyone other than A.
