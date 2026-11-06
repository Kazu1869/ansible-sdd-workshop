# Publishing instructions — no changes pushed by the generator

The linked repo `Kazu1869/ansible-sdd-workshop` has a minimal README on `main`. An alternate repo `jolohdy/aap-sdd-workshop` is named in the original brief. Resolve that discrepancy before publishing.

**Recommended:** keep instructor solution private and distribute `student-starter/` separately as an archive, or publish the instructor solution to a separate **private** repository; public branches are discoverable even if not the default branch.

To make a local feature branch of a clone and copy these files over (after owner approval):

```sh
git clone https://github.com/Kazu1869/ansible-sdd-workshop.git
cd ansible-sdd-workshop
git switch -c feature/sdd-workshop
# Copy generated repository files into this checkout, preserving .git/
git add -A
git diff --cached --check
git diff --cached --stat
git commit -m "Add specification-driven Ansible MOTD workshop"
# Only with explicit approval:
# git push -u origin feature/sdd-workshop
```

For participant distribution, archive the **contents** of `student-starter/` only. GitHub Actions validation is intentionally scoped to the complete instructor solution; don't enable the same gate on unfinished starter content.
