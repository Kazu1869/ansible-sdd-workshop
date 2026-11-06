# Ansible SDD best practices

1. Define *behavioral outcomes* first: EARS-style REQ identifiers and observable acceptance tests.
2. Design the role interface before tasks. `meta/argument_specs.yml` is a machine-readable **main entry point** contract; `defaults/main.yml` supplies runtime defaults. Do not rely on the `default` metadata to initialize a variable.
3. Validate non-schema rules before any mutation. A type check alone cannot guarantee a path's ownership, secure symlink handling, or a non-blank message.
4. Prefer built-in idempotent modules (`ansible.builtin.copy`, `ansible.builtin.file`, `ansible.builtin.assert`) and fully-qualified names. Never use `shell` to write a file that `copy` can manage.
5. Preserve least privilege. This lab uses `localhost`, lab-owned files, and no `become`.
6. Test success, missing required input, invalid choices, invalid types, business-rule failures, no side effects, and second-run idempotency. Keep negative playbooks excluded from lint's runnable scope.
7. Keep CI small: YAML, syntax check, role docs, lint, and test scripts; review every diff and add no secrets.
8. AI is an optional implementation assistant, not the specification approver: narrow prompts, approved examples, untouched-path constraints, independent review, and test evidence.
9. The complete instructor solution must not be part of the student distribution by default.

References: https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-argument-validation , https://docs.ansible.com/projects/lint/ , https://redhat-cop.github.io/automation-good-practices/ , https://roadmap.sh/vibe-coding/best-practices .
