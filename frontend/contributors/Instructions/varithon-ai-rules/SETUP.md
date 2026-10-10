# Drop-in instructions

Copy everything in this folder into the root of your repo, keeping the paths:

    docs/ai/...        the canonical rules — the ONLY place you edit rules
    CLAUDE.md          stub
    AGENTS.md          stub (Codex, Antigravity, most others)
    .cursor/rules/     stub
    .devin/            stub

Then, before any implementer starts:

1. A writes every `src/modules/<m>/<m>.contract.js` — typedefs, zod schemas, function list
2. A writes `src/constants/roles.js`, `enrollment.js`, `facility.js`
3. Announce CONTRACTS LOCKED
4. One branch per person: `a/...` `b/...` `c/...` `d/...`
5. Only then do implementers start

Checklist before letting the AIs loose:

- [ ] all seven docs/ai files present
- [ ] four adapter stubs in place
- [ ] 50-OWNERSHIP.md catch-all row present — no file unowned
- [ ] contracts written and LOCKED
- [ ] one branch per person, nobody commits to main
- [ ] glossary banned-synonym list read out to the team
