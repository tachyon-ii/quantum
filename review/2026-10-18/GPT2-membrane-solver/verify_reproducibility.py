#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""Re-run the strict command twice; compare generated physical/audit evidence.

The same failed scientific gate is reproducible evidence, not a physics pass.
Wall-clock timings, platform telemetry and absolute output paths are excluded.
"""
from __future__ import annotations
from pathlib import Path
import json
import subprocess
import sys
from models.binding.membrane.reporting import write_json
from models.binding.membrane import constants as C


EXCLUDED = {'elapsed_seconds', 'elapsed', 'started', 'platform', 'python'}


def scientific(value):
    if isinstance(value, dict):
        return {k: scientific(v) for k, v in value.items() if k not in EXCLUDED}
    if isinstance(value, list):
        return [scientific(v) for v in value]
    return value


def main():
    root = Path(__file__).resolve().parent
    outputs, returns = [], []
    for name in ('first', 'second'):
        directory = root / 'verification_runs' / name
        result = subprocess.run([sys.executable, '-m', 'models.binding.membrane.run_all',
                                 '--output-dir', str(directory)], cwd=root, capture_output=True, text=True)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'command.log').write_text(result.stdout + result.stderr)
        returns.append(result.returncode)
        outputs.append(directory / 'results')
    filenames = ('acceptance.json', 'audit.json', 'calibration.json', 'D.json', 'T.json', 'He3.json', 'He4.json', 'comparison.json')
    comparisons = []
    for filename in filenames:
        paths = [directory / filename for directory in outputs]
        if not all(path.exists() for path in paths):
            comparisons.append({'file': filename, 'equal': False, 'reason': 'missing generated file'})
            continue
        data = [scientific(json.loads(path.read_text())) for path in paths]
        comparisons.append({'file': filename, 'equal': data[0] == data[1]})
    equal = returns[0] == returns[1] and all(row['equal'] for row in comparisons)
    runs = [json.loads((directory / 'run.json').read_text()) if (directory / 'run.json').exists() else {} for directory in outputs]
    # An identically crashing implementation is not a successful replay.
    no_implementation_error = all(run.get('status') not in (None, 'implementation_error') for run in runs)
    hashes = [run.get('provenance', {}).get('source_tree_sha256') for run in runs]
    source_consistent = hashes[0] is not None and hashes[0] == hashes[1]
    success = equal and no_implementation_error and source_consistent
    report = {'status': 'physical_audit_outputs_reproduced' if success else 'reproduction_failed',
              'return_codes': returns, 'run_states': [run.get('status') for run in runs],
              'software_test_counts': [run.get('software_tests', {}).get('passed') for run in runs],
              'source_hashes': hashes, 'source_consistent': source_consistent,
              'comparisons': comparisons, 'excluded_telemetry_keys': sorted(EXCLUDED),
              'qualification': 'Reproduction is not a scientific acceptance pass; inspect run_states and acceptance.json.'}
    write_json(root / 'reproducibility.json', report)
    print(json.dumps(report, indent=C.JSON_INDENT))
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
