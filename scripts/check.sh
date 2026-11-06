#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
for tool in python3 ansible-playbook ansible-doc ansible-lint yamllint; do
  command -v "$tool" >/dev/null || { echo "BLOCKED: missing $tool; see README.md setup" >&2; exit 2; }
done
python3 scripts/sync_agents.py --check
python3 scripts/check_template.py
yamllint -c .yamllint .
ansible-playbook -i localhost, -c local playbooks/site.yml --syntax-check
ansible-doc -t role managed_file -r roles >/dev/null
ansible-lint --offline roles/managed_file playbooks/site.yml
python3 -m unittest discover -s tests -v
