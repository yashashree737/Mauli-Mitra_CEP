# 60-WORKFLOW — stage gates and handoff

## Agent order — by dependency, not by which tool is smartest

| # | Role | Runs | Does |
|---|---|---|---|
| 1 | Scaffolder | alone | Repo structure, config, ownership map |
| 2 | Contract author | alone | Every `*.contract.js`, all typedefs and zod schemas. LOCKED at the end of this stage. |
| 3 | Implementers | parallel | One per module, path-scoped, own branch. OPEN blocks they own, only. |
| 4 | Integrator | alone | Merges, resolves conflicts, runs the suite |
| 5 | Reviewer | alone | A different tool than the implementer |

Step 3 is only safe because step 2 finished completely.
If implementation starts while contracts still move, no amount of file marking saves you.

## Stage gates

| Gate | Meaning |
|---|---|
| MAP DONE | models, permission grid, modules, one traced flow — photographed |
| CONTRACTS LOCKED | every `*.contract.js` written and frozen. Implementation may begin. |
| UI FREEZE | no new page layouts. Styling tweaks only. |
| MOCK GREEN | full click-through works on mock data |
| DEMO BUILD | deployed, demo-able, rehearsed once |
| FEATURE FREEZE | no new features. Validation, demo and submission only. |

## Handoff format — append to `modules/<module>.md`

    ## Handoff <date time> — <who>
    Done:      <what works and was committed>
    Broken:    <what does not work, and the symptom>
    Next:      <the single next thing to do>
    Blocked:   <what you need from a human, or "nothing">

## Rules for agents

- Do not do another role's work because it looks unfinished. Report it.
- Do not fix a bug outside your owned paths. Log it.
- Run the linter before ending your turn.
- One task ticket, one branch, one concern. Do not bundle refactors into feature work.
- Every turn ends with either committed work or an entry in a module doc. Never silence.
