# 00-README — Router

Authoritative rule set for this repo. Read this file before any edit.

Project: **Vari Sathi** — helps a first-time Warkari join the Wari.

Two runtimes, one product:

    frontend/   Next.js (JavaScript)   camelCase
    backend/    FastAPI (Python)       snake_case

The API boundary is the ONLY place these two meet. See 20-ARCHITECTURE.

## Precedence order (highest first)

1. explicit instruction in the current task ticket
2. `modules/<module>.md` (most specific)
3. `40-EDIT-POLICY.md` (safety, never overridden by style)
4. `30-CONVENTIONS.md`
5. `20-ARCHITECTURE.md`
6. `10-CONTEXT.md`

Conflict you cannot resolve -> STOP. Append to `/docs/ai/CONFLICTS.md`.
Do not choose. Do not proceed on assumption.

## The five rules that matter most

1. Three layers only: `router -> service -> repository`. Nothing else.
2. Do not create functions that are not already listed in the module's contract.
3. Never edit a LOCKED file or LOCKED block.
4. Not your path in `50-OWNERSHIP.md`, not your edit.
5. **The wire format is snake_case. The frontend converts at the fetch boundary, nowhere else.**

## Scope discipline

Every feature must trace to one of three newcomer unknowns:
U1 how organised the Wari is · U2 which dindi will take me · U3 the route and safety.

If a requested change traces to none of them, STOP and log it. Do not build it.

## Time budget reality — read before proposing anything

Backend has ~10 effective hours for ~10.5 hours of work. Frontend the same.
There is no slack. The cut list in `10-CONTEXT.md` is already decided.
**Do not propose additions.** Do not "improve" a module beyond its contract.
An agent that adds a nice-to-have is spending hours the team does not have.

## File map

| File | Read it for |
|---|---|
| 10-CONTEXT.md | what the product is, glossary, banned words, cut list |
| 20-ARCHITECTURE.md | layers, modules, models, API contract, the case boundary |
| 30-CONVENTIONS.md | Python rules, JS rules, and the line between them |
| 40-EDIT-POLICY.md | what you may and may not touch |
| 50-OWNERSHIP.md | who owns which path |
| 60-WORKFLOW.md | stage gates, handoff format |
| modules/*.md | per-module contract and task queue |
