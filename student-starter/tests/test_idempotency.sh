#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
command -v ansible-playbook >/dev/null || { echo 'ansible-playbook is required' >&2; exit 2; }
export ANSIBLE_CONFIG="$ROOT/ansible.cfg"
mkdir -p lab-output
OUT="$(mktemp)"
DEST="$ROOT/lab-output/motd-idempotency-${OUT##*/}"
trap 'rm -f "$OUT" "$DEST"' EXIT
ansible-playbook -i localhost, -c local playbooks/valid.yml -e "rhel_motd_path=$DEST" >/dev/null
ansible-playbook -i localhost, -c local playbooks/valid.yml -e "rhel_motd_path=$DEST" >"$OUT"
if ! grep -E 'changed=0([[:space:]]|$)' "$OUT" >/dev/null; then
  cat "$OUT"; echo 'FAIL: repeated execution changed files' >&2; exit 1
fi
echo 'PASS: REQ-005 second run changed=0'
