# Ansible SDD workflow

The main conversation coordinates the work. Each specialist has a narrow ownership boundary and returns a structured handoff. Creating files alone does not schedule model calls or run an agent service.

| Stage | Owner | Input | Output / gate |
| --- | --- | --- | --- |
| Specify | spec-author | user goal, constraints, policy | numbered draft spec and REQ-to-test table |
| Assess readiness | spec-reviewer | draft + original goal | readiness recommendation; human scope acceptance before build |
| Implement | playbook-writer | accepted spec + owned file list | bounded roles/playbooks diff |
| Test | test-writer | accepted spec + test scope | independent expected values and acceptance tests |
| Validate | validation-runner | frozen snapshot + approved commands | actual versions, exit codes and NOT_RUN checks |
| Review | code-reviewer + compliance-reviewer | same frozen snapshot + evidence | correctness findings and control-by-control assessment |
| Resolve | responsible writer, then reviewers | concrete findings | tested fix; previous reviews invalidated where relevant |
| Accept | human / authorized maintainer | all evidence + residual risks | acceptance or requested changes |

Run writers sequentially by default. Parallelize final reviews after writes finish. For a small task, skip unnecessary authoring work but keep relevant validation and review. Respect prior authorization rather than repeatedly asking to approve the same scope. New dependencies, remote targets, privilege or policy exceptions require an actual decision if not already authorized.

## Start a feature

Copy specs/SPEC-TEMPLATE.md to a new SPEC-NNN file. Keep SPEC-001 as a runnable reference until its role/tests are deliberately replaced. In Codex, use `$ansible-sdd-workflow`; in Claude Code use `/ansible-sdd-workflow`. Supply the feature goal and spec path. See TOOLING.md for exact examples and availability limits.

## Gate and evidence rules

PASS is specific to the role's assigned checks. CHANGES_REQUIRED identifies a defect, failed test or failed applicable control. BLOCKED identifies missing policy, ambiguity, tools or evidence. A compliance table may mark individual controls NOT_APPLICABLE with rationale or UNKNOWN; UNKNOWN cannot support an overall compliance PASS. Neither a passing test nor an AI review certifies organizational compliance.

Use REVIEW-TEMPLATE.md. The coordinator records a baseline commit plus the diff and untracked-file hashes (or commits the exact reviewed snapshot). Reviews must cover the same bytes. Relevant changes require new validation/review. Review agents return findings; writers repair them. After two unsuccessful repair cycles, stop and explain the remaining blocker.

## Adapting for real Ansible/AAP work

Replace the example spec, policy and tests together with your project's authorized target/privilege model. Keep production inventories and credentials out of this starter. Introduce collections via declared requirements, with versions and verified module docs. Add Molecule for OS/service integration when valuable. For AAP, explicitly specify execution environment, inventory, credential references, project/collection dependencies, job/workflow inputs, RBAC ownership, check-mode limitations and rollback. This template does not configure or deploy AAP.
