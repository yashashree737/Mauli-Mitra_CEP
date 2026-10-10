# 50-OWNERSHIP — path to owner

Longest glob wins. Not your path, not your edit.
Only a human edits a LOCKED path.

| Path glob | Owner | Status |
|---|---|---|
| `docs/ai/**` | A (architect) | LOCKED |
| `backend/app/modules/*/contract.py` | A (architect) | LOCKED |
| `backend/app/constants/**` | A (architect) | LOCKED |
| `backend/app/models/**` | A + B | LOCKED after contract freeze |
| `backend/app/core/errors.py` | A | LOCKED |
| `frontend/src/lib/api.js` | A | LOCKED |
| `frontend/src/lib/case.js` | A | LOCKED |
| `backend/app/main.py`, `core/**` | B | OPEN |
| `backend/app/modules/auth/**` | B | OPEN |
| `backend/app/modules/users/**` | B | OPEN |
| `backend/app/modules/dindi/**` | B | OPEN |
| `backend/app/modules/enrollment/**` | B | OPEN |
| `backend/app/modules/route/**` | B | OPEN |
| `backend/app/modules/facility/**` | B | OPEN |
| `backend/app/modules/safety/**` | B | OPEN |
| `backend/app/modules/assistant/**` | B | OPEN — after 10:45 PM only |
| `backend/app/seed/**` | B | OPEN |
| `frontend/src/app/**` (golden path) | **A only** | OPEN |
| `frontend/src/components/**` | A | OPEN |
| `frontend/tailwind.config.js` | A | OPEN |
| `frontend/src/app/pramukh/**` | C | OPEN — A reviews every diff |
| `frontend/src/app/admin/**` | C | OPEN — A reviews every diff |
| `seed/**` (json data files) | C and D | OPEN |
| `content/**` | C and D | OPEN |
| `docs/SRS.md`, `docs/testing/**` | D | OPEN |
| `README.md` | D | OPEN |
| **`**` (catch-all)** | **A** | **ask before editing** |

No file is unowned. If a path is not listed, the catch-all applies: STOP and ask A.

**Golden-path pages are A's alone.** Landing, dindi list, dindi detail, enroll,
my-dindi and journey are never edited by C, D, or an AI tool acting for them.

One branch per person: `a/...` `b/...` `c/...` `d/...`
Nobody commits to `main`. A merges.
Frontend and backend are separate deploys — a broken one must not block the other.
