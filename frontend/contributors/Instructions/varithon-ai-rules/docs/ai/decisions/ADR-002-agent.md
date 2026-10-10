# ADR-002 — Vari Sahayak stays dumb

Status: accepted
Date: 2026-08-29

## Decision

The AI agent is one FastAPI endpoint. It filters rows from Postgres, puts them in the
prompt, and answers only from them. No vector DB, no embeddings, no LangChain, no RAG.

## Why

Done this way it is ~2 hours. Done "properly" it is ~5, and those 3 hours come directly
out of the enrollment module, which is the golden path. A judge cannot see the difference
between a retrieval pipeline and a filtered query in a 3-minute demo. They can very
much see a broken enroll button.

## Constraint

It must never invent a dindi, a facility, or a route stop. If the filtered rows do not
answer the question, it says so and points at the FAQ. A hallucinated facility on a
pilgrimage route is a safety failure, and it is the first thing a judge will probe.

## Gate

Not started before 10:45 PM, and only if F1-F5 are green.
