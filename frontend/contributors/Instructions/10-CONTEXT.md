# 10-CONTEXT — Product, vocabulary, and what is already cut

## Product

**Vari Sathi.** A first-time Warkari does not join the Wari because of three unknowns:

- **U1** — they do not know how organised the Wari already is
- **U2** — they do not know which dindi will take them
- **U3** — they fear the route: the distance, the villages, the safety

Vari Sathi removes all three before the person leaves home.

## Golden path — the flow that must always work

    Landing (Wari explained)
      -> Find a dindi (filter: village / language / route)
      -> Dindi detail + verified badge -> Enroll
      -> My Journey (day-wise route, km, halt villages, facilities)
      -> Safety kit (SOS, share live location)

Nothing outside this path may be built while any part of it is broken.

## Users

| Actor | Wants |
|---|---|
| Guest | to understand the Wari and browse verified dindis |
| Warkari (user) | to find and join a dindi, then see their journey |
| Dindi Pramukh | to review and approve who joins their dindi |
| Admin | to verify dindis and publish notices |

## Team and capacity

| | Role | Owns |
|---|---|---|
| A | Frontend, architect, git owner, integrator | `frontend/`, all contracts, merges |
| B | Backend + AI agent (FastAPI) | `backend/` |
| C | Seed data, content, pramukh/admin pages, PPT | `seed/`, `content/`, off-path pages |
| D | SRS, testing, feedback log, README, demo prep | `docs/` |

C and D are not developers. Pages they generate with AI are reviewed by A before merge,
and are **only ever off the golden path**.

## Already cut — do not rebuild these

| Cut | Replaced by | Why |
|---|---|---|
| `notice` module (backend) | static notices from seed data, rendered by C | saves B ~1h he does not have |
| Interactive facility map | facilities grouped as a list by day | map is 1.5h + a mobile rendering risk |
| App-wide Marathi toggle | Marathi on the landing page only | scope, not value |
| WhatsApp bot | a slide describing it as next phase | Business API verification is not obtainable in 24h |
| Forum | nothing | traces to no U |
| Payment gateway | UPI deep link only, if donation survives at all | traces to no U |

**If an agent proposes any of the above, refuse and cite this table.**

## Vari Sahayak (the AI agent) — gating and hard rules

- Not started before **10:45 PM**, and only if F1–F5 are green.
- **No vector DB, no embeddings, no LangChain, no RAG framework.**
  Pull the relevant rows from Postgres by filter, put them in the prompt, answer from them.
- It must never invent a dindi, a facility, or a route stop. If it does not know, it says so.
  A hallucinated facility on a pilgrimage route is a safety failure.
- If asked something outside dindi / route / facility / Wari basics, it declines and
  points at the FAQ.

## Glossary — use the left column, never the right

| Use this | Banned synonyms |
|---|---|
| Dindi | group, batch, team, troupe, party |
| Warkari | pilgrim, member, participant, traveller |
| Pramukh | leader, admin, head, manager, organiser |
| Enrollment | registration, booking, application, joining |
| RouteStop | halt, stop, waypoint, node, checkpoint |
| Facility | amenity, service, resource, POI, station |
| Notice | announcement, alert, post, bulletin |
| Wari | yatra, pilgrimage, march |

Signing up for an account is **auth/signup**.
Joining a dindi is **enrollment**. These are never mixed.

Applies to Python identifiers, JS identifiers, API fields, UI copy and commit messages alike.
Python renders these snake_case (`route_stop`), JS camelCase (`routeStop`) — same word, different case.

## Non-negotiable constraints

- **Mobile first.** Every screen is built at 380px, then widened. A Warkari has a phone.
- Weak network, low tech literacy. Big targets, few taps, plain language.
- Marathi place names must render correctly. UTF-8 end to end, in both runtimes.
- Vegetarian and religious context — content must be respectful and accurate.
- No real personal data anywhere. Invented names in all seed files.
