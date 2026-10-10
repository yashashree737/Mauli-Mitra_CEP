# ADR-001 — Stack

Status: accepted
Date: 2026-08-29

## Decision

Split stack. Next.js (JavaScript) frontend, FastAPI (Python) backend, Postgres, SQLModel.
Wire format is snake_case. No TypeScript.

## Why

B is strongest in Python and owns the whole backend plus the AI agent.
A is a frontend developer. Forcing one language would slow the person it was forced onto.
FastAPI also makes the agent endpoint cheap — it is one more router.

## Cost we accepted

Two deploys, CORS, two env files, and a casing boundary. Budgeted at ~2 hours.

## What replaces TypeScript

1. **Pydantic** at every route boundary — bad data rejected at the door, and it is
   also the contract file the AI tools read
2. **Type hints everywhere** in Python; JSDoc typedefs on shared frontend shapes
3. **Enums instead of string literals** — `Role.PRAMUKH`, never `"pramukh"`

## Consequence

The casing boundary is the highest-risk bug in the project. It is contained by making
`frontend/src/lib/api.js` and `case.js` LOCKED files that convert exactly once.
No aliases in Pydantic. See 20-ARCHITECTURE.
