---
name: ansible-sdd-workflow
description: Coordinate specification-first Ansible development with dedicated spec, writer, validation and review agents. Use for an end-to-end SDD feature or change.
---

Read AGENTS.md, docs/WORKFLOW.md, agents/REGISTRY.yml and policies/automation.yml from the repository root. Remain in the main conversation as coordinator; subagents return to you rather than dispatching the whole workflow themselves.

1. Inspect the request, baseline commit, target environment and selected spec. Reuse accepted decisions; ask only for material missing scope. For a new feature, delegate spec-author to draft a numbered spec. Have spec-reviewer assess readiness in a fresh read-only context. Block implementation for contradictions or unaccepted scope.
2. Delegate playbook-writer with the accepted spec and exact file ownership. Delegate test-writer with the same spec and separate test ownership. Prefer sequential writes; never let either change the other's artifacts or rewrite acceptance criteria.
3. Freeze the snapshot, including untracked files. Delegate validation-runner to inspect and run the approved local checks. Missing tools/evidence is BLOCKED; failures are CHANGES_REQUIRED. Do not treat syntax/lint success as runtime validation.
4. Once checks pass and writers have stopped, delegate code-reviewer and compliance-reviewer in parallel against the same snapshot. Give them raw artifacts and test evidence, not author conclusions. Wait for both. If native agents are unavailable, load each canonical role with a supported subagent tool; if no subagents exist, use sequential role passes and state that review was not independent.
5. Route findings back to the responsible writer, rerun affected checks and rereview changed artifacts. Stop after two unsuccessful fix cycles with the blocker. Do not weaken tests/policy or hide uncertainty.
6. Summarize changes, REQ/control coverage, executed and NOT_RUN checks, unresolved risks and human acceptance needed. Save review evidence only within requested scope. Never publish, merge, deploy or target production without user authorization.

Use docs/REVIEW-TEMPLATE.md at each handoff. An agent recommendation is not human approval, regulatory certification or evidence that an unexecuted check passed.
