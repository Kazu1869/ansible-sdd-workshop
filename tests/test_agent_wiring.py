"""Verify adapter drift fails closed and regeneration restores consistent content."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AgentWiring(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='sdd-wiring-')
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        for folder in ('agents', '.agents', '.claude', '.codex', 'scripts'):
            shutil.copytree(ROOT / folder, self.project / folder, ignore=shutil.ignore_patterns('__pycache__'))

    def sync(self, check=True):
        command = [sys.executable, str(self.project / 'scripts/sync_agents.py')]
        if check:
            command.append('--check')
        return subprocess.run(command, text=True, capture_output=True, timeout=20)

    def test_rejects_stale_role_and_repairs_adapter(self):
        source = self.project / 'agents/spec-reviewer.md'
        source.write_text(source.read_text() + '\nCheck the new requirement.\n')
        result = self.sync()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('.codex/agents/spec-reviewer.toml', result.stderr)
        self.assertEqual(self.sync(check=False).returncode, 0)
        self.assertEqual(self.sync().returncode, 0)

    def test_rejects_extra_adapter_and_repairs_skill_copy(self):
        extra = self.project / '.claude/agents/stale.md'
        extra.write_text('Unexpected agent')
        skill = self.project / '.claude/skills/ansible-write-tests/SKILL.md'
        skill.write_text('Stale skill')
        self.assertEqual(self.sync().returncode, 1)
        self.assertEqual(self.sync(check=False).returncode, 0)
        self.assertFalse(extra.exists())
        self.assertEqual(self.sync().returncode, 0)
