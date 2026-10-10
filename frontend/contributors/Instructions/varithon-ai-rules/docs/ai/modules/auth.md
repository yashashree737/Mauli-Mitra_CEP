# Module: auth

Owner: B
Contract file: `src/modules/auth/auth.contract.js` (LOCKED)
Traces to: U2 — the person must have an account before enrolling

## Purpose

Signup, login, session. Nothing about dindis. Signing up is NOT enrollment.

## Public function list — this list is complete

```
model:   findByPhone(phone)
         create(userData)
service: signup(payload)
         login(phone, otp)
         getSession(token)
routes:  POST /api/auth/signup
         POST /api/auth/login
         GET  /api/auth/me
```

Do not add to this list. If you need another function, write it under
**Contract change requests** below and end your turn.

## Tasks

- [ ] (add task tickets here)

## Contract change requests

_(empty — append: what you need, why, proposed signature)_

## Assumptions

_(empty — append anything you assumed instead of asking)_

## Handoffs

_(append using the format in 60-WORKFLOW.md)_
