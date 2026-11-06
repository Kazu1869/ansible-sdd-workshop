---
name: ansible-write-spec
description: Draft measurable Ansible specifications before implementation. Use for the spec-author stage of an Ansible SDD task.
---

Read AGENTS.md and agents/COMMON.md from the repository root, then follow agents/spec-author.md. Load the selected spec and policies/automation.yml. Obtain the coordinator's exact scope and reviewed snapshot; report missing inputs as BLOCKED.

Use the role's ownership and handoff contract. Delegate to the named native agent `spec-author` when the runtime supports it and the coordinator requests an independent context. Otherwise apply the role sequentially and disclose the fallback. Do not recursively launch another agent from inside the same role.

Return the docs/REVIEW-TEMPLATE.md fields, evidence and next owner. Do not widen scope, edit another role's files, assert unexecuted checks passed, or grant release approval.
