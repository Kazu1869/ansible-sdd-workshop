# Phase 4 — Contract tests (12 minutes) + quality (6 minutes)

From the student starter root, run:

```sh
bash tests/test_contract.sh
bash tests/test_idempotency.sh
ansible-playbook -i localhost, -c local playbooks/invalid/missing_text.yml
ansible-playbook -i localhost, -c local playbooks/invalid/invalid_environment.yml
```

The last two commands are **expected to exit nonzero**. Correct behavior is validation failure, not a successful play. The test script prints `PASS` for each negative case only if its failure left the output unchanged. Invalid environment and invalid type should be rejected by role argument validation before task execution. Blank text and unsafe path are separate task assertions, which also precede changes.

Final 6 minutes:

```sh
ansible-doc -t role rhel_motd -r roles
ansible-lint roles/rhel_motd playbooks/valid.yml
yamllint -c .yamllint .
```

Use the Ansible VS Code extension for YAML editing and diagnostics; command-line Ansible validates the actual contract. Do not assume the editor automatically suggests every custom role variable.

**Troubleshooting:** `role not found` → run from starter root and inspect `ansible.cfg`; `required argument` → check `meta/argument_specs.yml` and the valid playbook; `permission denied` → use the workspace as your current user; unexpected `changed=1` on repeat → inspect rendered content/permissions. `ansible-doc` role arguments require a compatible ansible-core version.
