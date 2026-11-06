# Phase 3 — Implement role behavior (10 minutes)

Fill `roles/rhel_motd/tasks/main.yml` in the student starter. Prefer `ansible.builtin.assert` before any filesystem tasks, then `ansible.builtin.file` for directory/absent state and `ansible.builtin.copy` with `content` for the banner. All tasks require names and fully qualified module names.

Business rules to implement: non-blank text; destination must be directly under `lab-output/`; mode must match a four-character octal pattern like `0644`; enabled creates the directory and writes; disabled removes the managed file. No `become`, no `/etc/motd`.

```sh
ansible-playbook -i localhost, -c local playbooks/valid.yml
cat lab-output/motd
```

**Expected file:** first line `[TEST]`, second line `Authorized access only.`. First run typically reports `changed=2` (directory and file); subsequent runs report `changed=0`. The initial count may differ if a directory already exists.

**Checkpoint:** the role writes to the workspace and can be run again without changes.
