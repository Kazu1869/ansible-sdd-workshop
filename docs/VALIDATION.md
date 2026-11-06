# Template validation — 2026-11-06

## Environment and deterministic checks

Python 3.12.14, ansible-core 2.20.11, ansible-lint 26.11.0, yamllint 1.38.0. The requirements declare compatible ranges rather than a reproducible lockfile. Run `bash scripts/check.sh` in your own environment after adaptation.

The validation command covers generated-adapter drift detection, seven native agent schemas, eight skill frontmatter/UI metadata records, YAML, example playbook syntax, role documentation, Ansible lint, and seven Python test methods. The acceptance suite exercises valid content/mode, required/invalid input (present and absent destination), preserved content/mode on rejection, enabled and disabled idempotency, non-mutating check mode, and both directory/file symlinks in enabled/disabled states. Generator tests deliberately introduce stale role text, an extra agent and a stale skill copy, then verify rejection and regeneration.

## Review evidence

Two separate read-only agent contexts reviewed workflow/client usability and the compliance skill on the actual example. This is not a test of all seven native agents inside each vendor client. The reviews found staged-diff omissions in the handoff instructions, a missing validation-document link, and a directory-symlink check that used a trailing `/.`. The handoff now compares against the explicit baseline; this document supplies the link target; the role now stats the exact output directory. The symlink acceptance test exposed the original failure before correction.

Structured final review evidence is retained in `reviews/template-review.md`. Local execution outcomes and remote CI are recorded there or reported alongside publication; this document does not predeclare the result of a future GitHub run.

## Limitations

- Native TOML/Markdown formats and discovery paths were checked against official docs linked in TOOLING.md. Actual Codex/Claude client loading, native tool restrictions, model access and paid agent calls are not covered by CI. Claude Code is not installed in the build environment.
- The separate review contexts used the canonical instructions in the hosted tool runtime. They do not prove native client discovery. A fallback must always be disclosed.
- Acceptance checks exercise only the bundled localhost example. New roles, collections, inventories, AAP integration or privileges require appropriate specs, policies and tests.
- Check mode avoids copying when the directory does not yet exist; it demonstrates no mutation, not a complete rendered diff for that case.
- Symlink checks reject static symlink paths, but do not defend against a malicious process racing path checks. Do not use this as production filesystem confinement.
- LOCAL-* controls are a local example policy, not CIS, STIG, Red Hat support validation or regulatory certification.
- GitHub Actions runs deterministic checks only; agent verdicts are recommendations and do not constitute human acceptance or deployment approval.
