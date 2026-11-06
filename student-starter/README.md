# Participant starter — Ansible SDD MOTD

This is an **intentionally incomplete** role: participants first define `roles/rhel_motd/meta/argument_specs.yml`, then implement `roles/rhel_motd/tasks/main.yml`. Do not expect contract/idempotency tests to pass until phases 2 and 3 are finished.

Work from this directory as the repository root. Read `specs/SPEC-001-rhel-motd.md`, then follow:

1. [`lab/01-requirements.md`](lab/01-requirements.md) — 5 min.
2. [`lab/02-contract.md`](lab/02-contract.md) — 12 min.
3. [`lab/03-implementation.md`](lab/03-implementation.md) — 10 min.
4. [`lab/04-validation.md`](lab/04-validation.md) — 18 min total (12 + 6).

The optional AI exercise is `lab/05-ai-assisted.md`.

```sh
ansible --version
ansible-playbook -i localhost, -c local playbooks/valid.yml --syntax-check
```

All changes are restricted to `lab-output/` and never need sudo. If you need packages, use a virtualenv and `pip install -r requirements-dev.txt`. Do not browse the instructor solution during the exercise.
