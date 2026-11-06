# AI development guardrails (optional)

- Read `specs/SPEC-001-rhel-motd.md` first; identify requirement IDs before editing.
- The public contract is `roles/rhel_motd/meta/argument_specs.yml`; runtime defaults are in `defaults/main.yml`. Never invent public variables or change existing names without review.
- Scope each request to named files; propose the change and state assumptions. Do not touch `.github/workflows/`, `instructor/`, or `recovery/` without explicit permission.
- Keep the workshop `localhost`-only, no privilege escalation or writes outside `lab-output/`; never introduce secrets or remote dependencies.
- Use `ansible.builtin.*` FQCNs, descriptive task names, minimal dependencies, and idempotent modules.
- Create acceptance tests for positive, negative, side-effect, and second-run behavior. Never weaken tests to mask defects.
- After each change: inspect `git diff`, run `yamllint -c .yamllint .`, `ansible-lint`, `bash tests/test_contract.sh`, and `bash tests/test_idempotency.sh` (where available).
- Report which tests passed, failed, or were not run; disclose assumptions and changed dependencies. AI output must be reviewed before commit.

Keep one feature per AI session and give an example to follow. Use `lab/05-ai-assisted.md` for scoped Spec → Build → Review → Explain prompt examples.
