# Security

## Always
- **Validate and sanitize at trust boundaries**; allow-list over deny-list; enforce limits (size, length, rate).
- **AuthN/AuthZ**: check authorization on every request server-side, by object (prevent IDOR/BOLA), not just by route. Default deny.
- **Secrets**: never hardcode/commit/log. Use env/secret manager. If you find a leaked secret, report immediately and recommend rotation; do not paste it into outputs.
- **Injection**: parameterized queries, safe templating, no `eval`/shell string building; use argument arrays for subprocesses; escape output for its context (HTML/JS/URL/SQL).
- **Passwords/keys**: use vetted libraries and strong hashing (argon2id/bcrypt/scrypt); never invent crypto; TLS everywhere; constant-time comparisons for secrets.
- **Sessions/tokens**: short-lived, scoped, rotated, httpOnly/secure/sameSite cookies; validate JWT signature/claims/audience/expiry.
- **File handling**: validate type/size/path; prevent path traversal; store uploads outside web root; scan if feasible.
- **SSRF/CSRF/XSS/CORS**: restrict outbound targets, use CSRF protection for cookie auth, CSP, narrow CORS origins.
- **Dependencies**: prefer maintained, pinned packages; run the ecosystem audit (`npm audit`, `pip-audit`, `cargo audit`, etc.); review new transitive additions; check licenses.
- **Least privilege**: DB users, service accounts, CI tokens, container user (non-root), IAM roles.
- **Logging**: audit security events; never log secrets, tokens, full card numbers, or PII.
- **Errors**: generic messages to clients, detail in logs.

## Security review checklist (high-risk changes)
- [ ] Threat considered: who can call this, with what data, what's the worst outcome?
- [ ] AuthZ tested for each role, including negative cases
- [ ] Input validation + output encoding in place
- [ ] No secrets in diff, config, tests, or logs
- [ ] New dependencies vetted
- [ ] Data at rest/in transit protection appropriate; PII minimized
- [ ] Rate limiting / abuse cases handled
- [ ] Rollback and incident contact known

## Scope note
This skill supports defensive and normal development work. Do not write exploit code or attack tooling; for suspected vulnerabilities, describe the issue, impact, and remediation.
