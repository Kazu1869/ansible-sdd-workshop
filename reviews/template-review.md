# Template review and execution record — 2026-11-06

## Snapshot and scope

Baseline: `a96ef693d4fc19df43a20cfcac44f884b9d64706` (instructor workshop on main).

Reviewed template source snapshot: SHA-256 `529118807aa15e3f9e27cd7eae167b99879b7f5eaeb6209339096c8ac51999c7` of `git diff --binary <baseline> --`, including all staged sources. No untracked source files were omitted. This final evidence document is appended afterward; implementation, policy, specs, agents, skills and tests are unchanged from that snapshot.

Two independent read-only agent contexts reviewed the canonical workflow/usability and exercised the compliance-review skill on SPEC-001 v1.0 (REQ-001–REQ-006). They read artifacts and diffs but did not execute the validation commands. The coordinator executed local validation separately. These were hosted review contexts, not native Codex/Claude discovery tests.

## Findings and disposition

| Finding | Severity | Correction | Rereview |
| --- | --- | --- | --- |
| Plain git diff omitted staged changes from review evidence | P2 | COMMON.md and generated adapters now compare against an explicit baseline and include untracked hashes | Usability reviewer PASS |
| README linked a missing validation document | P3 | Added docs/VALIDATION.md | Usability reviewer PASS |
| Directory stat used lab-output/. and followed an intermediate symlink | High | Stat exact lab-output and target entries, reject symlinks before mutation | Compliance reviewer closed; acceptance suite passed |

Final usability assessment: PASS for assigned scope, no remaining actionable findings. Native-client loading remains explicitly unverified.

Final compliance assessment: PASS within the bundled local-example scope, no open findings. It is a recommendation, not certification or human release approval.

| Control | Assessment | Evidence |
| --- | --- | --- |
| LOCAL-001 | PASS | Localhost/local connection, become false, fixed output paths, symlink regression cases |
| LOCAL-002 | PASS within inspected scope | No candidate secrets observed in inspected source diff or supplied evidence |
| LOCAL-003 | PASS | Required/nonblank content checks and exact-path symlink refusal before mutation; invalid-input/symlink tests |
| LOCAL-004 | PASS | FQCN assert/stat/file/copy, lint, enabled/disabled second-run checks |
| LOCAL-005 | PASS for selected versions | Declared ranges and actual versions below |
| LOCAL-006 | PASS | REQ-to-test mapping, rollback, frozen snapshot, retained handoff and execution record |

The compliance review's final message preceded the final combined-check completion. The completed combined result below is the coordinator's execution evidence, not a claim that the reviewer ran tests.

## Executed checks

Python 3.12.14; ansible-core 2.20.11; ansible-lint 26.11.0; yamllint 1.38.0.

| Check | Exit code | Observed outcome |
| --- | --- | --- |
| bash scripts/check.sh | 0 | All constituent checks passed |
| Adapter synchronization | 0 | 30 generated native agent/skill adapter files match canonical sources |
| Template wiring/metadata | 0 | Seven role schemas, eight skills and required project documents |
| yamllint -c .yamllint . | 0 | No YAML errors |
| Example syntax and role documentation | 0 each | Playbook parsed; role documentation generated |
| ansible-lint --offline roles/managed_file playbooks/site.yml | 0 | 0 rule failures, 0 rule warnings |
| python3 -m unittest discover -s tests -v | 0 | Ran 7 methods in 35.205s; OK |
| Skill creator quick_validate.py for each canonical skill | 0 each | All eight reported Skill is valid |
| git diff --check | 0 | No whitespace errors |

The seven methods covered check mode, exact content/mode and repeat execution, disabled repeat, invalid inputs on existing/missing targets, file/directory symlinks in enabled/disabled states, stale role regeneration, and extra-agent/stale-skill repair. Subcases are included within the methods.

Non-fatal notices: the installed Ansible internal bundled collection lacked a MANIFEST.json, and ansible-lint reported directory expansion. They did not fail any check.

## NOT_RUN / remaining limits

- Native client discovery/execution and vendor tool restrictions; no Claude Code client installed. Deterministic schemas and hosted review contexts do not prove those integrations run end to end.
- Showroom, remote hosts, AAP, privileged automation, organizational standards and adversarial filesystem races.
- GitHub Actions outcome is reported alongside publication; no remote success is predeclared here.

Next owner: student/maintainer to adapt the generic spec, role, policy and tests, then validate in their actual environment. No deployment or regulatory approval is implied.
