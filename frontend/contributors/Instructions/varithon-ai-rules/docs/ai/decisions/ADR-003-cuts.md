# ADR-003 — Scope cuts

Status: accepted
Date: 2026-08-29

## Decision

Cut: the `notice` backend module, the interactive facility map, the app-wide Marathi
toggle, the WhatsApp bot, the forum, and any payment gateway.

## Why

Measured capacity is ~10 effective coding hours for backend and ~10 for frontend,
against ~10.5 hours of scoped backend work alone. The cuts close that gap.
Notices become static seed content. The map becomes a list grouped by day, which
removes a mobile rendering risk at the same time.

## Consequence

These are decided, not open. An agent proposing to rebuild any of them should be
refused with a pointer to the CUT table in 10-CONTEXT.md.
