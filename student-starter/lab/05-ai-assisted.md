# Optional extension — AI-assisted SDD (up to 90 minutes total)

AI is optional; participants must approve the contract themselves. The goal is **specification → build → review → explain**, not accepting unreviewed generated tasks.

## Scoped prompts

**Spec**: "Read `specs/SPEC-001-rhel-motd.md`. Identify ambiguous requirements and propose acceptance tests mapped to REQ-001..REQ-007. Do not write code; list assumptions."

**Build**: "Follow `AGENTS.md`. Using approved SPEC-001 and `roles/rhel_motd/meta/argument_specs.yml`, implement only `roles/rhel_motd/tasks/main.yml`. Use `ansible.builtin` FQCNs, localhost workspace-only paths, no privileges, no new variables. Explain the intended diff before edits."

**Review**: "Review `git diff` for requirement coverage, unexpected files, interface changes, dangerous paths, secrets, non-idempotent modules, and validation before mutation. Do not modify files. Report risks with file/line references."

**Tests**: "Using the contract and REQ IDs, inspect `tests/test_contract.sh` and suggest positive, negative, no-side-effect, and idempotency checks. Only change tests with explicit approval. Report executed versus unexecuted checks."

**Explain**: "Explain how main entry-point validation happens before the role's normal tasks, and which rules need explicit assertions. Cite the implementation files and distinguish runtime behavior from assumptions."

## 90-minute suggested allocation

| Activity | Minutes |
| --- | ---: |
| Entire manual core lab | 45 |
| Git feature branch, reviewable commits | 10 |
| Optional AI prompt + independent diff review | 15 |
| Expanded negative tests / nested argument spec demonstration | 10 |
| GitHub Actions and optional Molecule discussion | 10 |

Follow https://roadmap.sh/vibe-coding/best-practices : keep project context lean, plan narrowly, provide a reference example, protect off-limit files, review diffs, and run tests after edits. No AI service is required to finish the core lab.
