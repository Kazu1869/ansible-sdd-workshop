# Agent and skill locations

| Purpose | Canonical source | Loaded by |
| --- | --- | --- |
| Shared project rules | AGENTS.md | Codex; Claude through CLAUDE.md import |
| Dedicated role contracts | agents/COMMON.md + agents/*.md + REGISTRY.yml | coordinator and adapter generator |
| Native Codex agents | .codex/agents/*.toml | current local Codex clients supporting standalone custom agents |
| Native Claude agents | .claude/agents/*.md | Claude Code project subagents |
| Canonical project skills | .agents/skills/*/SKILL.md | Codex project skill discovery |
| Claude project skills | .claude/skills/*/SKILL.md | Claude Code project skill discovery |

These are repository-scoped assets. Cloning does not install personal ChatGPT skills, grant credentials, bypass trust prompts, or start autonomous background agents. No model is pinned; native agents inherit your selected model. Your account must provide its own model access.

## Codex

Launch your local Codex client from the cloned project root and accept project trust only after reviewing it. Select a listed skill, or enter:

```text
Use $ansible-sdd-workflow. Add a feature from specs/SPEC-002-example.md.
Use the dedicated agents, keep writer scopes disjoint, and wait for both
code-reviewer and compliance-reviewer before summarizing the results.
```

For a narrow pass:

```text
Use the spec-reviewer subagent to review specs/SPEC-001-managed-file.md.
Report readiness and REQ gaps without changing files.
```

Standalone TOML agents use name, description and developer_instructions. Older clients using different configuration formats may not discover them; use the canonical agents/*.md instructions explicitly or update the client. Parent permissions still apply: a read-only instruction is not a separate filesystem sandbox. The review adapters disable shell/apps/plugins, but do not claim to enforce all possible write mechanisms.

## Claude Code

Start `claude` in the repository root. Use `/agents` to inspect the seven project agents. Start a new session if definitions created after session startup are not listed. Run:

```text
/ansible-sdd-workflow Develop the feature in specs/SPEC-002-example.md.
```

Or ask directly: `Use the compliance-reviewer subagent to assess the current diff against policies/automation.yml.` Reviewers allow only Read, Glob and Grep. Writers allow file edits; validation-runner has Bash for checks. Bash can write files, so its local-only scope is an instruction and the parent's sandbox remains important. No bypass-permissions mode or blanket tool approval is configured.

## ChatGPT Work / other agents

A repository clone does not automatically install these definitions into hosted ChatGPT. Ask the main agent to read AGENTS.md, agents/COMMON.md and the selected role files, then spawn supported subagents with those instructions. If delegation is unavailable, run sequential role passes and disclose that there was no independent review. The Markdown instructions remain usable in other assistants; native discovery is client-specific.

## Maintain adapters

Edit canonical agents/*.md or .agents/skills/, then run:

```sh
python3 scripts/sync_agents.py
python3 scripts/sync_agents.py --check
bash scripts/check.sh
```

The generator embeds complete shared/role instructions in both native formats and copies skills for Claude, avoiding symlink requirements on Windows. CI rejects missing, stale or extra generated adapters. agents/openai.yaml is skill UI metadata, not a subagent definition.

## Official references checked 2026-11-06

- [Codex custom subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex local skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code skills](https://code.claude.com/docs/en/skills)

Native formats are structurally checked here. End-to-end client discovery must be verified in the learner's actual installed client; provider/model permissions and UI behavior are not exercised by the deterministic CI suite.
