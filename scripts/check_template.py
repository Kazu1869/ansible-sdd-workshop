#!/usr/bin/env python3
"""Validate template wiring, canonical skill metadata and native adapter schemas."""
import re
import tomllib
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def frontmatter(path):
    text = path.read_text()
    assert text.startswith('---\n'), f'Missing frontmatter: {path}'
    header, body = text[4:].split('\n---\n', 1)
    return yaml.safe_load(header), body


def main():
    registry = yaml.safe_load((ROOT / 'agents/REGISTRY.yml').read_text())['agents']
    names = [r['name'] for r in registry]
    assert len(names) == len(set(names)) == 7
    for role in registry:
        name = role['name']
        assert (ROOT / role['instructions']).is_file()
        assert role['access'] in ('review', 'execute', 'write')
        assert (ROOT / f".agents/skills/{role['skill']}/SKILL.md").is_file()
        data = tomllib.loads((ROOT / f'.codex/agents/{name}.toml').read_text())
        assert data['name'] == name and data['description'] == role['description']
        assert data['developer_instructions'].strip()
        # Permissions belong to the parent session, never an agent-file override.
        assert not {'sandbox_mode', 'approval_policy', 'model', 'model_provider'} & data.keys()
        header, body = frontmatter(ROOT / f'.claude/agents/{name}.md')
        assert header['name'] == name and body.strip()
        if role['access'] == 'review':
            assert set(header['tools'].split(', ')) == {'Read', 'Glob', 'Grep'}
            assert data['features']['shell_tool'] is False
    skills = list((ROOT / '.agents/skills').glob('*/SKILL.md'))
    assert len(skills) == 8
    for skill in skills:
        header, body = frontmatter(skill)
        assert set(header) == {'name', 'description'}
        assert header['name'] == skill.parent.name
        assert re.fullmatch(r'[a-z0-9-]{1,64}', header['name'])
        assert header['description'].strip() and body.strip()
        metadata = yaml.safe_load((skill.parent / 'agents/openai.yaml').read_text())['interface']
        assert '$' + header['name'] in metadata['default_prompt']
    for name in ('README.md', 'AGENTS.md', 'CLAUDE.md', 'docs/WORKFLOW.md', 'docs/TOOLING.md',
                 'docs/REVIEW-TEMPLATE.md', 'docs/VALIDATION.md', 'policies/automation.yml', 'specs/SPEC-TEMPLATE.md'):
        assert (ROOT / name).is_file(), name
    print('PASS: seven agent roles, eight skills, native schemas and project wiring')


if __name__ == '__main__':
    main()
