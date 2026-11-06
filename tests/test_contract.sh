#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
command -v ansible-playbook >/dev/null || { echo 'ansible-playbook is required' >&2; exit 2; }
export ANSIBLE_CONFIG="$ROOT/ansible.cfg"
# Do not touch the tracked example output. The tests supply a unique safe path.
mkdir -p "$ROOT/lab-output"
TESTDIR="$(mktemp -d "$ROOT/lab-output/test.XXXXXX")"
trap 'rm -rf "$TESTDIR"' EXIT
DEST="$ROOT/lab-output/motd-contract-${TESTDIR##*/}"
ABSENT="$DEST-absent"
trap 'rm -f "$DEST" "$ABSENT"; rm -rf "$TESTDIR"' EXIT
run(){ ansible-playbook -i localhost, -c local "$@"; }
run playbooks/valid.yml -e "rhel_motd_path=$DEST" >"$TESTDIR/valid.log" 2>&1 || { cat "$TESTDIR/valid.log"; exit 1; }
EXPECTED="$(printf '[TEST]\nAuthorized access only.')"
ACTUAL="$(cat "$DEST")"
[[ "$ACTUAL" == "$EXPECTED" ]] || { printf 'Unexpected MOTD: %s\n' "$ACTUAL"; exit 1; }
[[ $(stat -c '%a' "$DEST") == 644 ]] || { echo 'FAIL: incorrect banner mode' >&2; exit 1; }
printf 'PASS: REQ-003 valid banner content and mode\n'
BEFORE="$(sha256sum "$DEST" | cut -d' ' -f1)"
for case in missing_text invalid_environment invalid_type blank_text unsafe_path invalid_mode; do
  CASE_DEST="$DEST"
  if [[ "$case" == unsafe_path ]]; then
    # Use an isolated forbidden target outside lab-output, never a shared fixed path.
    CASE_DEST="${TMPDIR:-/tmp}/ansible-sdd-unsafe-$$"
    [[ ! -e "$CASE_DEST" ]] || { echo 'Unsafe test destination already exists' >&2; exit 1; }
  fi
  if run "playbooks/invalid/${case}.yml" -e "rhel_motd_path=$CASE_DEST" >"$TESTDIR/$case.log" 2>&1; then
    echo "FAIL: $case unexpectedly succeeded" >&2; exit 1
  fi
  AFTER="$(sha256sum "$DEST" | cut -d' ' -f1)"
  [[ "$AFTER" == "$BEFORE" ]] || { echo "FAIL: $case modified target" >&2; exit 1; }
  if [[ "$case" == unsafe_path ]]; then
    [[ ! -e "$CASE_DEST" ]] || { echo 'FAIL: unsafe destination created' >&2; exit 1; }
  fi
  echo "PASS: $case rejected without target mutation"
done
# A nonexistent file must also remain absent after contract validation failure.
if run playbooks/invalid/invalid_environment.yml -e "rhel_motd_path=$ABSENT" >"$TESTDIR/absent.log" 2>&1; then
  echo 'FAIL: invalid input succeeded with absent target' >&2; exit 1
fi
[[ ! -e "$ABSENT" ]] || { echo 'FAIL: invalid input created absent target' >&2; exit 1; }
echo 'PASS: invalid input never created absent target'
# Disabled state removes the managed file, then stays removed.
run playbooks/valid.yml -e "rhel_motd_path=$DEST" -e '{"rhel_motd_enabled": false}' >"$TESTDIR/disabled.log" 2>&1
[[ ! -e "$DEST" ]] || { echo 'FAIL: disabled banner not removed' >&2; exit 1; }
echo 'PASS: disabled removes file'
run playbooks/valid.yml -e "rhel_motd_path=$DEST" -e '{"rhel_motd_enabled": false}' >"$TESTDIR/disabled-again.log" 2>&1
[[ ! -e "$DEST" ]] || { echo 'FAIL: disabled file reappeared' >&2; exit 1; }
grep -E 'changed=0([[:space:]]|$)' "$TESTDIR/disabled-again.log" >/dev/null || { cat "$TESTDIR/disabled-again.log"; exit 1; }
echo 'PASS: disabled remains absent with changed=0'
