# Ansible SDD development template

A reusable starting point for specification-driven Ansible projects, with seven dedicated agent roles, eight skills, local acceptance tests and CI. This `sdd-template` branch is separate from the completed instructor workshop on `main`.

## Get your own working copy

```sh
git clone --branch sdd-template --single-branch --depth 1 https://github.com/Kazu1869/ansible-sdd-workshop.git my-ansible-project
cd my-ansible-project
git remote rename origin upstream
git switch -c feature/my-first-spec
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
bash scripts/check.sh
```

Use Python 3.12+ on Linux/WSL. The shallow single-branch clone checks out only this template. The upstream repository is public and its instructor workshop remains accessible separately. Add your own repository as `origin` when ready; do not push student work to the workshop upstream. No AI account is needed to run the deterministic checks.

## What is included

| Agent | Responsibility |
| --- | --- |
| spec-author | Draft requirements, interface and acceptance criteria |
| spec-reviewer | Check ambiguity, completeness and readiness |
| playbook-writer | Implement roles/playbooks within the accepted scope |
| test-writer | Write requirement-driven acceptance tests |
| validation-runner | Execute approved local checks and report exit codes |
| code-reviewer | Independently review correctness and test gaps |
| compliance-reviewer | Assess supplied control IDs and safety boundaries |

The main conversation coordinates the stages using the `ansible-sdd-workflow` skill. Each role also has its own skill. Native definitions live in [.codex/agents/](.codex/agents/) and [.claude/agents/](.claude/agents/); canonical instructions live in [agents/](agents/). See [tool setup and invocation](docs/TOOLING.md).

## Use it

1. Read [AGENTS.md](AGENTS.md) and [the workflow](docs/WORKFLOW.md).
2. Copy [the spec template](specs/SPEC-TEMPLATE.md) to a new numbered feature spec and describe your goal and constraints.
3. In Codex, invoke `$ansible-sdd-workflow`; in Claude Code, invoke `/ansible-sdd-workflow`. Provide the feature goal and spec path. Use dedicated agents when supported; fallback passes are labeled as single-agent work.
4. Review the spec, implementation, tests and control evidence. Run `bash scripts/check.sh` after changes. Agent recommendations do not replace human acceptance or deployment authorization.

## Runnable reference

The bundled [SPEC-001](specs/SPEC-001-managed-file.md) manages `lab-output/status.txt` on localhost without become. It demonstrates a required role input, idempotent writes, disabled-state removal, validation before changes and check mode.

```sh
ansible-playbook -i localhost, -c local playbooks/site.yml
cat lab-output/status.txt
ansible-playbook -i localhost, -c local playbooks/site.yml -e '{"managed_file_enabled": false}'
```

Tests use isolated temporary project copies; they do not replace your example output. Adapt the reference role/playbook/tests to your approved project. Extend [policies/automation.yml](policies/automation.yml) for your environment before authorizing other targets or privileges. The included LOCAL-* controls are an example baseline, not CIS/STIG certification.

## Validation

`bash scripts/check.sh` checks agent/skill synchronization and metadata, YAML, Ansible syntax/docs/lint, and acceptance tests for required/invalid input, unchanged targets on rejection, content/mode, enabled/disabled idempotency, check mode and symlink boundaries. CI runs the same command on pushes and pull requests; it makes no paid AI calls and uses no deployment credentials.

See [validation evidence and limits](docs/VALIDATION.md). The template does not install personal skills, deploy AAP, or launch agents without an AI client and user task.
