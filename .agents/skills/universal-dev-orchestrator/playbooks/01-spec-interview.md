# Spec before code (requirements interview)

**Hard gate**: no implementation until acceptance criteria exist and are confirmed. In autonomous runs where nobody can answer, log each assumption explicitly and proceed with the safest default.

## Interview rules
- Ask **one question at a time**; give your recommended default so the person can just say "yes".
- Look it up in the code first; only ask what the code cannot tell you.
- Challenge vague words ("fast", "simple", "secure", "users"): turn each into a measurable statement.
- Probe edges: roles/permissions, empty/error states, scale, data retention, existing data, rollout, who is affected if it breaks.

## Spec template (`.agent/spec.md`)
1. **Problem & users**: who, what pain, why now
2. **Scope / non-goals**: explicit exclusions
3. **User stories + acceptance criteria**: "Given/When/Then", each testable
4. **Data & API sketch**: entities, endpoints, key request/response fields, errors
5. **Non-functional**: performance targets, security/privacy, accessibility, compatibility, observability
6. **Risks & unknowns**: with how each will be resolved
7. **Definition of done**: which tests/gates must pass
8. **Open questions / assumptions log**

## Exit check
- [ ] Every acceptance criterion is observable and testable
- [ ] Non-goals listed
- [ ] High-risk areas flagged (auth, money, data migration, public contract)
- [ ] The requester confirmed, or assumptions are logged
