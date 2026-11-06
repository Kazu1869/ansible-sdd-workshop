# SPEC-001 — Standardized safe RHEL MOTD

**Status:** approved for workshop | **Version:** 1.0 | **Owner:** workshop instructor

## Intent
An operator can produce a consistent environment-labeled login-banner file safely in a workspace without privileged access. This simulates `/etc/motd` but must not modify it.

## Behavioral requirements (EARS)

- **REQ-001:** When the role is called, it shall reject calls that omit the banner text; whitespace-only text shall also be rejected before file changes.
- **REQ-002:** When an environment is provided, the role shall accept only `dev`, `test`, or `prod`, otherwise fail before file changes.
- **REQ-003:** When a valid enabled request is made, the role shall write the exact content `[ENVIRONMENT]` followed by a newline and the text, using the requested mode.
- **REQ-004:** If any interface or business-rule validation fails, the role shall not create, remove, or modify its target file.
- **REQ-005:** When the same valid request is repeated, the role shall report no changes on the second run.
- **REQ-006:** When management is disabled, the role shall remove its managed file if present and leave it absent subsequently.
- **REQ-007:** The automation shall only write/remove files directly inside its repository's `lab-output/` directory, never system paths, and shall not escalate privileges.

## Role public interface

| Argument | Type | Required | Runtime default | Validation |
| --- | --- | --- | --- | --- |
| `rhel_motd_text` | `str` | yes | none | must not be whitespace-only |
| `rhel_motd_environment` | `str` | no | `dev` | `dev`, `test`, `prod` |
| `rhel_motd_enabled` | `bool` | no | `true` | Ansible bool |
| `rhel_motd_mode` | `str` | no | `'0644'` | four-character octal starting with `0` |
| `rhel_motd_path` | `path` | no | `<repo>/lab-output/motd` | must be direct child of lab-output |

The role argument spec enforces types, required fields, and choices on the **main** entry point. Runtime defaults in `defaults/main.yml` control execution. Additional assertions enforce nonempty text, file-mode format, and destination safety.

## Expected output

For `rhel_motd_text: Authorized access only.` and `rhel_motd_environment: test`:

```text
[TEST]
Authorized access only.
```

The YAML literal block preserves a trailing newline on the output file. The tests compare command-substitution output, which strips terminal newlines.

## Traceability / acceptance

| ID | Verification | Test |
| --- | --- | --- |
| REQ-001 | Missing and blank text fail | `tests/test_contract.sh` |
| REQ-002 | Invalid environment fails | `tests/test_contract.sh` |
| REQ-003 | Correct header and contents | `tests/test_contract.sh` |
| REQ-004 | Invalid type, environment, mode, path, text leave file hash unchanged; absent stays absent | `tests/test_contract.sh` |
| REQ-005 | Second play has `changed=0` | `tests/test_idempotency.sh` |
| REQ-006 | Enabled=false removes the managed file | `tests/test_contract.sh` |
| REQ-007 | Invalid output destination is rejected | `tests/test_contract.sh` |

## Assumptions and exclusions

- The caller works from this repository; `playbook_dir` points at `playbooks/` and its parent is the workspace.
- A lab owner can write under `lab-output/`; symlinked destination files require separate security controls in production and are not a substitute for production-grade path confinement.
- No AAP controller, network infrastructure, real `/etc/motd`, secrets, and no privileged `become` operation.
- Rollback: set `rhel_motd_enabled: false` to remove the managed file, or remove the workspace output manually.
