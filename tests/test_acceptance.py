"""REQ-mapped behavior tests in an isolated temporary project, never live hosts."""
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ManagedFileAcceptance(unittest.TestCase):
    def setUp(self):
        (ROOT / 'lab-output').mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix='acceptance-', dir=ROOT / 'lab-output')
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)
        shutil.copytree(ROOT / 'roles', self.project / 'roles')
        self.output_dir = self.project / 'lab-output'
        self.dest = self.output_dir / 'status.txt'
        self.content = 'Hello from SDD.\n'
        self.env = dict(os.environ, ANSIBLE_CONFIG=str(ROOT / 'ansible.cfg'), ANSIBLE_NOCOLOR='1')
        self.env['ANSIBLE_ROLES_PATH'] = str(self.project / 'roles')

    def run_role(self, variables, check=False, success=True, error=None):
        playbook = self.project / 'case.json'
        playbook.write_text(json.dumps([{
            'name': 'Acceptance test', 'hosts': 'localhost', 'connection': 'local',
            'gather_facts': False, 'become': False, 'roles': ['managed_file'],
        }]))
        command = ['ansible-playbook', '-i', 'localhost,', '-c', 'local', str(playbook), '-e', json.dumps(variables)]
        if check:
            command.append('--check')
        result = subprocess.run(command, cwd=self.project, env=self.env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertRegex(result.stdout, error)
        return result.stdout

    def test_content_mode_and_idempotency(self):
        variables = {'managed_file_content': self.content}
        self.run_role(variables)
        self.assertEqual(self.dest.read_bytes(), self.content.encode())
        self.assertEqual(stat.S_IMODE(self.dest.stat().st_mode), 0o644)
        self.assertRegex(self.run_role(variables), r'changed=0\s')

    def test_invalid_inputs(self):
        cases = [
            ({}, r'missing required arguments.*managed_file_content'),
            ({'managed_file_content': '   '}, r'managed_file_content must be a nonblank string'),
            ({'managed_file_content': ['bad']}, r'(managed_file_content|nonblank string)'),
            ({'managed_file_content': self.content, 'managed_file_enabled': ['bad']}, r'managed_file_enabled'),
        ]
        for variables, error in cases:
            for present in (False, True):
                with self.subTest(variables=variables, present=present):
                    self.output_dir.mkdir(exist_ok=True)
                    self.dest.unlink(missing_ok=True)
                    if present:
                        self.dest.write_bytes(b'Existing sentinel\n')
                        self.dest.chmod(0o600)
                    before = (self.dest.read_bytes(), self.dest.stat().st_mode) if present else None
                    self.run_role(variables, success=False, error=error)
                    if present:
                        self.assertEqual((self.dest.read_bytes(), self.dest.stat().st_mode), before)
                    else:
                        self.assertFalse(self.dest.exists())

    def test_disabled(self):
        variables = {'managed_file_content': self.content}
        self.run_role(variables)
        variables['managed_file_enabled'] = False
        self.run_role(variables)
        self.assertFalse(self.dest.exists())
        self.assertRegex(self.run_role(variables), r'changed=0\s')
        self.assertFalse(self.dest.exists())

    def test_check_mode(self):
        variables = {'managed_file_content': self.content}
        self.run_role(variables, check=True)
        self.assertFalse(self.output_dir.exists())
        self.run_role(variables)
        before = (self.dest.read_bytes(), self.dest.stat().st_mode)
        variables['managed_file_content'] = 'Changed only in preview\n'
        self.run_role(variables, check=True)
        self.assertEqual((self.dest.read_bytes(), self.dest.stat().st_mode), before)
        variables['managed_file_enabled'] = False
        self.run_role(variables, check=True)
        self.assertEqual((self.dest.read_bytes(), self.dest.stat().st_mode), before)

    def test_symlink_boundaries(self):
        external = self.project / 'external'
        external.mkdir()
        sentinel = external / 'status.txt'
        sentinel.write_bytes(b'External sentinel\n')
        variables = {'managed_file_content': self.content}
        for directory_link in (True, False):
            for enabled in (True, False):
                with self.subTest(directory_link=directory_link, enabled=enabled):
                    if directory_link:
                        self.output_dir.symlink_to(external, target_is_directory=True)
                    else:
                        self.output_dir.mkdir()
                        self.dest.symlink_to(sentinel)
                    variables['managed_file_enabled'] = enabled
                    try:
                        self.run_role(variables, success=False, error=r'Output path must not be a symlink')
                        self.assertEqual(sentinel.read_bytes(), b'External sentinel\n')
                    finally:
                        if directory_link:
                            self.output_dir.unlink()
                        else:
                            self.dest.unlink()
                            self.output_dir.rmdir()
