# SPEC-001 — Local managed file example

Status: accepted example | Version: 1.0 | Owner: template maintainer
Acceptance scope: repository-local demonstration, authorized by the request for this template. New features need their own spec and scope decision.

## Intent and interface

Demonstrate a role contract without credentials, remote systems or elevated access. Manage only `<repo>/lab-output/status.txt`. Never overwrite a symlink at the output directory or target. Use Python 3.12+ with the declared dev dependencies; no external Ansible collections.

| Input | Type | Required | Runtime default | Validation |
| --- | --- | --- | --- | --- |
| managed_file_content | str | yes | none | actual string, nonblank |
| managed_file_enabled | bool | no | true | Ansible bool-convertible; use JSON booleans at CLI |

## Requirements

- REQ-001: When content is missing, non-string or blank, reject before mutation with role-validation or content-assertion evidence.
- REQ-002: When enabled, write content exactly as provided, with mode 0644, only to lab-output/status.txt on localhost without become.
- REQ-003: If inputs are invalid or lab-output/status.txt or lab-output is a symlink, reject before changing target bytes or mode; a missing target stays absent. Symlink errors identify the output path check.
- REQ-004: Repeating an enabled request shall report changed=0.
- REQ-005: When disabled, remove the managed file; repeating disable reports changed=0. Interface validation still applies.
- REQ-006: Check mode shall leave output bytes, permissions and existence unchanged, including when the output directory is absent.

## Acceptance and traceability

| REQ | Test in tests/test_acceptance.py | Expected result |
| --- | --- | --- |
| REQ-001 | test_invalid_inputs | invalid input rejected with expected error category |
| REQ-002 | test_content_mode_and_idempotency | exact bytes and 0644 |
| REQ-003 | test_invalid_inputs, test_symlink_boundaries | existing bytes/mode preserved, missing stays missing, external sentinel unchanged |
| REQ-004 | test_content_mode_and_idempotency | enabled repeat changed=0 |
| REQ-005 | test_disabled | absent and disabled repeat changed=0 |
| REQ-006 | test_check_mode | no mutation for present and absent output |

Run `bash scripts/check.sh`. Map LOCAL-001..LOCAL-006 in policies/automation.yml to this spec and its role/tests. Local acceptance tests use a temporary project copy under lab-output/ and never replace a user's example output.

## Rollback and exclusions

Set managed_file_enabled to false using a YAML/JSON boolean to remove the example file. The role leaves the empty output directory in place. No protection against a malicious process racing path checks; no production filesystem confinement claim. No remote service/OS integration, AAP deployment, organizational compliance certification, or Molecule requirement. Dependency ranges are checked at the installed versions, not every permitted release.
