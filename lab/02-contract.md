# Phase 2 — Contract before code (12 minutes)

Work in the **student starter** directory, from its root. Open `roles/rhel_motd/meta/argument_specs.yml`. Add a `main` entry-point specification with `short_description` and `options`. Define the public variables below; no `rhel_motd_text` default should exist.

| Variable | Type | Required | Choices | Default |
| --- | --- | --- | --- | --- |
| `rhel_motd_text` | `str` | true | — | none |
| `rhel_motd_environment` | `str` | false | dev/test/prod | dev |
| `rhel_motd_enabled` | `bool` | false | — | true |
| `rhel_motd_mode` | `str` | false | — | '0644' |
| `rhel_motd_path` | `path` | false | — | workspace path (runtime defaults) |

**Use `defaults/main.yml` for actual runtime defaults**. Leave the required text undefined. In particular, schema `default:` documents the contract but does not replace role defaults.

```sh
ansible-playbook -i localhost, -c local playbooks/valid.yml --syntax-check
ansible-doc -t role rhel_motd -r roles
```

**Checkpoint:** `ansible-doc` displays all five arguments; missing text is marked required. `--syntax-check` should succeed even before the task implementation exists.

**Recovery:** if stuck, ask the instructor for `recovery/02-contract/` (do not copy the full solution).
