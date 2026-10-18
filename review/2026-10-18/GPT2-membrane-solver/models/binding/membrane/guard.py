#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""AST plus import-hook firewall for the held-out targets."""
from __future__ import annotations
import ast
import importlib.abc
from pathlib import Path
import sys


def assert_targets_not_loaded():
    forbidden = [name for name in sys.modules if name.rsplit('.', 1)[-1] == 'targets']
    if forbidden:
        raise AssertionError(f'Held-out targets imported before compare: {forbidden}')


def static_audit(directory: Path):
    violations = []
    for path in sorted(directory.rglob('*.py')):
        if path.name == 'compare.py':
            continue
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ''] + [alias.name for alias in node.names]
            else:
                continue
            if any(module.rsplit('.', 1)[-1] == 'targets' for module in modules):
                violations.append(f'{path.relative_to(directory)}:{node.lineno}')
    if violations:
        raise AssertionError('Only compare.py may import targets: ' + ', '.join(violations))
    return {'status': 'pass', 'audited_python_files': len(list(directory.rglob('*.py')))}


class TargetFirewall(importlib.abc.MetaPathFinder):
    def __init__(self):
        self.comparison_phase = False

    def find_spec(self, fullname, path=None, target=None):
        if fullname.rsplit('.', 1)[-1] == 'targets' and not self.comparison_phase:
            raise ImportError('Held-out targets are sealed until compare.py runs last.')
        return None

    def install(self):
        assert_targets_not_loaded()
        sys.meta_path.insert(0, self)
        return self

    def enable_comparison(self):
        assert_targets_not_loaded()
        self.comparison_phase = True

    def remove(self):
        if self in sys.meta_path:
            sys.meta_path.remove(self)
