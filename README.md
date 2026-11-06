# Ansible SDD Workshop — RHEL MOTD

An instructor-led, **45-minute** hands-on exercise (with a **90-minute** extension) in specification-driven Ansible development. The target is a harmless `lab-output/motd` under this repository, never `/etc/motd`. Runs on `localhost` without `become`, AAP controller, containers, or credentials.

## Pick the right starting point

- **Participant:** use [`student-starter/`](student-starter/README.md). It deliberately has an unfinished role. Keep the instructor solution out of the learners' working directory; **do not distribute this complete repository to participants**.
- **Instructor:** the complete solution with CI validation is in `roles/`, `playbooks/`, and `tests/`; read [`instructor/README.md`](instructor/README.md).
- **Specification:** [`specs/SPEC-001-rhel-motd.md`](specs/SPEC-001-rhel-motd.md) is the behavioral contract; `roles/rhel_motd/meta/argument_specs.yml` is the role interface contract.

## Prerequisites and setup

Use a Linux terminal in the [Ansible Dev Tools Showroom](https://rhpds.github.io/ansible-dev-tools-showroom/modules/index.html) with Python 3.11+, `ansible-playbook`, `ansible-doc`, `ansible-lint`, `yamllint`, and the Ansible VS Code extension. Verify first:

```sh
ansible --version
ansible-lint --version
yamllint --version
```

If the tools are not installed and package installation is permitted, provision a Python virtualenv:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

The Showroom's provided environment may already contain these tools. No `ansible-galaxy` collections are needed.

## Run complete instructor solution

```sh
ansible-playbook -i localhost, -c local playbooks/valid.yml
ansible-doc -t role -l -r roles
ansible-doc -t role rhel_motd -r roles
bash tests/test_contract.sh
bash tests/test_idempotency.sh
yamllint -c .yamllint .
ansible-lint
```

The playbook writes `lab-output/motd` inside the workspace. Inspect it using `cat lab-output/motd`. Tests use isolated temporary directories and do not modify that example file.

## Publishing

The destination is [`Kazu1869/ansible-sdd-workshop`](https://github.com/Kazu1869/ansible-sdd-workshop), confirmed by the repository owner. This repository is public, including the instructor solution and recovery snippets. Distribute only the contents of `student-starter/` to learners at the start of class; the public solution is discoverable, so this setup is appropriate for guided practice, not a closed-answer assessment. See `instructor/PUBLISHING.md` for additional distribution guidance; its original destination-confirmation note is historical.

## Safety / implementation notes

- No root, SSH, network targets, credentials, or system files.
- `rhel_motd_text` is mandatory; do not create a default for it. `rhel_motd_path` has a safe workspace-derived default and is restricted to a path inside `lab-output/` by a separate business rule. Existing targets outside this directory are never written.
- A YAML/JSON boolean `rhel_motd_enabled: false` (CLI: `-e '{"rhel_motd_enabled": false}'`) removes the managed file; the interface is validated even when disabled.
- For portability, `ansible.builtin.copy` uses inline `content` and `mode` (string `"0644"`) rather than requiring a template file.
- This lab uses native role argument validation. The underlying Ansible version, not VS Code completion, is the authoritative enforcer.

Documentation: [Ansible roles argument specifications](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-argument-validation), [ansible-lint](https://docs.ansible.com/projects/lint/), [Red Hat automation good practices](https://redhat-cop.github.io/automation-good-practices/).
