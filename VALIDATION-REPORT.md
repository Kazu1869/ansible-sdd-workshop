# Review and validation — 2026-11-06

## Scope

Reviewed the supplied complete workshop archive against the destination repository's placeholder README. The owner explicitly selected `Kazu1869/ansible-sdd-workshop` and requested direct publication. The repository is public; its solution and recovery files are discoverable. Use the participant starter for guided practice rather than a closed-answer assessment.

## Findings corrected before publication

- The disable test used key=value extra vars, passing `false` as a string. With ansible-core 2.20 this failed boolean condition evaluation, despite passing interface validation. Both instructor and participant test scripts now pass a JSON boolean. The README documents this CLI form.
- Tests used fixed output names and could remove an existing lab file. Both sets now derive unique output names from temporary allocations.
- Added file-mode verification and a repeated-disable check (`changed=0`) to cover REQ-003 and REQ-006 more fully.
- Updated both YAML lint configurations to match ansible-lint's YAML rules; the original produced a configuration warning.
- Updated the main README's obsolete destination-confirmation note and removed its unverified claim of CI success. Instructor publishing notes are retained as supplied and the README identifies their destination-confirmation note as historical.

## Executed validation

**All checks listed below passed.**

Environment: Python 3.12.14, ansible-core 2.20.11, ansible-lint 26.11.0, yamllint 1.38.0. Dependencies installed from the supplied requirements without changes.

- `yamllint -c .yamllint .`
- `ansible-playbook -i localhost, -c local playbooks/valid.yml --syntax-check`
- `ansible-doc -t role rhel_motd -r roles`
- `ansible-lint --offline` (bundled rules, no schema refresh)
- `bash tests/test_contract.sh`: exact two-line banner, default mode, six invalid cases with unchanged target content, absent target on invalid input, disable, repeated disable.
- `bash tests/test_idempotency.sh`: enabled second run reports `changed=0`.
- Bash syntax checks for participant scripts and `git diff --check`.
- Separate participant-root smoke test with the completed contract and tasks copied in; the published starter remains intentionally incomplete.

## Remaining limits

- The actual Showroom image and live 45-minute schedule have not been tested.
- Runtime validation covers the installed versions, not every version allowed by the dependency ranges.
- This is a trusted local workspace lab. Destination symlinks and adversarial filesystem changes are outside its confinement guarantee, as disclosed by the specification. Do not use it as a hardened production role.
- Negative tests check nonzero failure and unchanged content; they do not match the exact validation error or compare every metadata field.
- GitHub Actions status is reported separately after publication; this record does not predeclare a green remote run.
