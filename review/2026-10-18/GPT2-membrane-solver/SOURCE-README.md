# Membrane solver — source package

This package contains all 21 Python source files, including tests. It excludes
Git internals, bytecode caches, and precomputed scientific results.

## Run from this directory

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest models/binding/membrane/tests -q
python -m models.binding.membrane.run_all
```

The strict production run writes its own report and results. With the supplied
specification, the previously executed production run stopped at the isolated
capsid volume acceptance test. Passing software tests does not establish passing
scientific acceptance tests or a calibrated physical model.

The source here is byte-for-byte identical to the Python source in the original
membrane_solver_gpt6_astra_pro.zip delivery. SOURCE-MANIFEST.sha256 lists hashes.
