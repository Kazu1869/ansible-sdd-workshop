# Instructor runbook

**Never distribute this full checkout at the beginning.** It contains the completed role. Distribute a ZIP made from `student-starter/` only. Keep the solution in the instructor checkout or a private branch; only share recovery snippets as needed.

## 45-minute schedule

| Time | Activity | Instructor checkpoint |
| --- | --- | --- |
| 00:00–00:05 | Requirements | REQ IDs and acceptance discussed |
| 00:05–00:17 | Role argument contract | `ansible-doc -t role rhel_motd -r roles` |
| 00:17–00:27 | MOTD implementation | file shows `[TEST]` and text |
| 00:27–00:39 | Positive, negative, idempotency | contract script passes |
| 00:39–00:45 | Docs, lint, recap | lint/check outcomes noted |

## 90-minute session

Run the above 45-minute lab, then follow `lab/05-ai-assisted.md` for branches, scoped AI assistance, tests, and CI. Tool-specific AI commands are not assumed to exist.

## Preflight / readiness checklist

- [ ] Distribute **only** `student-starter/`, zipped at its directory root; avoid showing solution paths in shared editor.
- [ ] Showroom accessible to participants; terminal/VS Code working.
- [ ] `ansible --version`, `ansible-doc`, `ansible-lint`, and `yamllint` are available; Python 3.11+.
- [ ] A workspace path is writable by the participant without sudo.
- [ ] Run `bash tests/test_contract.sh` and `bash tests/test_idempotency.sh` on instructor checkout.
- [ ] Test the starter's setup and recoveries in the **actual** Showroom image (not guaranteed by local CI).
- [ ] Display the SPEC and show that argument validation happens before normal role tasks.
- [ ] Prepare the `recovery/02-contract` and `recovery/03-tasks` files separately.
- [ ] GitHub destination and PR strategy confirmed; do not expose instructor solution via public default branch before class.

## Expected check outputs

`tests/test_contract.sh` prints positive-banner PASS, six rejected-and-unchanged PASS lines, absent target PASS, and disable PASS. `tests/test_idempotency.sh` prints `PASS: REQ-005 second run changed=0`. `ansible-doc` lists `rhel_motd` argument options. Negative standalone playbooks fail nonzero by design. Ansible itself prints version-dependent error text.

## Live troubleshooting

| Symptom | Resolution |
| --- | --- |
| Role not found | `cd` into starter root; confirm `ansible.cfg` relative role path |
| No validation error for missing input | inspect `argument_specs: main: options:` indentation and spelling |
| `rhel_motd_text` missing from defaults | intentional: required input only |
| File unexpectedly created on invalid input | validation/assertions must run before file operations |
| Unexpected output path | starter playbooks live in `playbooks/`; `playbook_dir | dirname` is repo root |
| Weird file permissions | quote `'0644'`, avoid numeric YAML parsing |
| Lint reports on incomplete tasks | only run lint after implementation; in CI the instructor solution is checked |
| Wrong CLI flags | run `ansible-doc --help`; role docs use `-t role -r roles` |

## Separation of concerns

Core Ansible role entry-point argument validation is provided by ansible-core. It validates types and choices (not arbitrary string contents, path security, or atomicity across multiple tasks). Assertions before mutations cover the latter business constraints at the workshop level. The role is a **lab artifact**, not a hardened system configuration role.

## Reference attribution and license notes

The implementation is original and does not copy third-party source. Patterns are inspired by `ansible-assistant` (behavioral spec and Spec/Build/Review/Explain), `sdd-ansible-codex` (traceability and review), `ansible-ci-demo` (GitHub Actions and idempotency), and the roadmap.sh vibe-coding review guidance. No substantial external code or catalog content was imported, avoiding unverified redistribution rights. Before importing future third-party source, inspect its repository license.
