# Membrane solver
<!-- Implementer: OpenAI ChatGPT — GPT-6 Astra Pro -->

An executable implementation of **BUILD-SPEC-membrane-solver.md**, retaining the supplied energy functional rather than silently repairing it. The original build document is included verbatim.

## Run

From the extracted `membrane_solver` directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m models.binding.membrane.run_all
```

The script also works directly:

```sh
python models/binding/membrane/run_all.py
```

The default command writes:

```text
models/binding/membrane/report.md
models/binding/membrane/results/run.json
models/binding/membrane/results/acceptance.json
models/binding/membrane/results/audit.json
models/binding/membrane/results/calibration.json
models/binding/membrane/results/D.json
models/binding/membrane/results/T.json
models/binding/membrane/results/He3.json
models/binding/membrane/results/He4.json
models/binding/membrane/results/comparison.json
models/binding/membrane/results/software-tests.txt
models/binding/membrane/results/software-tests.xml
```

**With the supplied functional, the expected production outcome is a failed isolated-capsid acceptance gate, not a table of fitted nuclear predictions.** The all-vertex optimizer converges; the reference-volume criterion fails. Exact computed values are in the generated report. A nonzero exit in this case is not an installation error.

Exit codes: `0` = requested computation finished; `2` = scientific/software gate failure, or diagnostic run demonstrating a failed gate; `3` = interrupted numerical run, runtime budget exhaustion, or implementation error. Diagnostic and tests-only modes do not imply a completed production study.

## Other reproducible commands

Software tests, without running the scientific acceptance workflow:

```sh
python -m pytest models/binding/membrane/tests -q
```

Additional **uncalibrated diagnostics**, including a finer isolated mesh, doubled area penalty, and the bending variant:

```sh
python -m models.binding.membrane.run_all --mode diagnostics --output-dir diagnostics
```

Two independent processes, checking that physical/audit results reproduce while explicitly excluding wall-clock telemetry:

```sh
python verify_reproducibility.py
```

The reproducibility checker does not change any reported number. It compares generated JSON from two runs, writes its own JSON evidence, and exits nonzero on a difference.

The production scan defaults to every specified reach. The spec-permitted reduced scan is explicit:

```sh
python -m models.binding.membrane.run_all --two-deltas
```

That selects the smallest and largest declared reaches, records the choice, and never fits the reach. A finite wall-time budget is enforced. The runtime of a complete calibrated study has **not** been established: the strict production run stops before calibration at the first scientific gate.

## Architecture

```text
models/binding/membrane/
  constants.py        Physical inputs, numerical settings, added-setting ledger
  targets.py          Held-out values; imported only by compare.py
  mesh.py             Icospheres, surface geometry, signed local plane gaps
  energy.py           Literal energy and float64 PyTorch derivatives
  relax.py            SciPy L-BFGS-B, exact affine centroid constraints
  calibrate.py        Nested D/He4 calibration; singlet arithmetic audit
  paths.py            Area-weighted loads, contact continuation, roll and spin
  analyse.py          Patch metrics, charge radii, quartic and quantum calculations
  chain.py            Collinear starts and constrained separation scans
  guard.py            Static and runtime target-import firewall
  reporting.py        JSON, provenance and report tables
  run_all.py          Orchestration and fail-fast scientific gates
  compare.py          Final held-out comparison, with no feedback into fitting
  tests/              Software tests and dependency-staged scientific gates
  results/            Generated evidence
```

No centre coordinates are independent optimization variables. Mesh vertices are the mechanical variables. Affine projection fixes the whole-system vertex centroid to machine precision. For constrained scans, specified skin-centroid or frozen-vertex constraints are imposed on those same vertex variables.

Adhesion counts both skins without a half factor. KD candidates are rebuilt for each objective evaluation. Derivatives include the source vertex and the target face's moving plane. Interior classification uses conservative KD-accelerated ray/triangle parity, with solid-angle winding for ambiguous edge hits. Convexity is not assumed for the inside test.

Discrete candidate selection, inside/outside classification and graph switches are not differentiated. Autograd supplies the ordinary derivative within a fixed branch. The software gradient tests explicitly avoid crossing the piecewise fade branches. No smoothing term has been added to improve convergence.

All physical parameters, numerical tolerances, force/scan limits and added algorithmic choices are declared in `constants.py`. Integer literals used for dimensions, array indices, algebraic factors, CLI return codes and mesh topology are structural code, not extra fitted physical constants. Prediction-only values are confined to `targets.py`.

## What was actually exercised

The packaged `report.md`, JSON, test log and JUnit XML are written by the code. The software tests check geometry, inside/outside signs, both-skin adhesion accounting, moving-target gradients, rigid covariance, centroid projection, Coulomb and graph rules, optimization stationarity, quantum discretization, import isolation, and workflow failure handling.

Tests that mock a converged state or a response function are explicitly marked **synthetic workflow fixtures**. They test calibration/continuation/reporting control flow and are never used as scientific output. Their existence is not evidence that a calibrated nuclear relaxation or peel trajectory succeeded.

The default scientific run executes the all-vertex isolated test at the prescribed primary mesh and stops on its failure. Downstream modules are implemented, but their **calibrated physical predictions and full-study convergence are not validated** under the supplied spec. The generated nucleus files explicitly say `not_run` rather than containing plausible-looking placeholders.

## Specification issues preserved, not patched

`SPEC-ISSUES.md` explains the algebra. In brief:

* The inflation term has a nonzero expansive first derivative at the rest geometry, whereas the quadratic area penalty has zero first derivative there. The isolated reference sphere is not stationary for a finite area penalty.
* The analytic rest area/volume differ from the triangulated rest geometry. This is retained exactly as specified, not normalized away.
* The stated singlet mesh formula calibrates the **patch-only** binding, but the functional applies slingshot to the connected singlet too. Both literal rules are retained and their disagreement is computed.
* The fixed mesh-neighbourhood search can become shorter than the adhesion reach on the finer mesh. The report shows where this occurs.

Additional interpretation choices are enumerated in the report: front-width sampling, charge-radius origin, local-neighbour absence, force-area reweighting, scan frame, force limits, and constrained-profile versus verified saddle terminology. They are not hidden in a diagram or a fitted crease factor.

## Outputs after the gates are satisfied

A subsequent, explicitly revised physical specification can use the implemented production path. For each reach and each separately calibrated primary/quadratic/bending variant, the code is wired to write energies, radii, pair patches, per-vertex contact maps, frozen-P1 quartic samples, quantum solutions when confining and numerically resolved, force-step trajectories, inversion observations, Kabsch spin, and chain separation scans. NPZ snapshots contain editable vertex coordinates and face topology, not rendered substitutes.

Mesh sensitivity uses unchanged fit parameters for the comparison. A specified finer-mesh promotion triggers a new calibration and applicable gates at the reporting mesh. Area-penalty sensitivity holds the calibration parameters fixed and repeats the computed measurement families. Undefined measurements cannot be asserted to pass sensitivity.

The code distinguishes a measured contact-loss load, a censored force scan, and an optimizer failure. It does not equate numerical failure with a demonstrated saddle-node. No polarization-sign mapping is implemented.

## Reproducibility and provenance

The repository includes a local Git commit. `report.md` records that commit, a source-tree hash, the original build-spec hash, dependency versions, precision, platform and thread count. Generated reports/results, test caches and verification runs are ignored by Git. Dependency versions in `requirements.txt` match the environment used for the packaged run; the `+cpu` build suffix on PyTorch is omitted from the portable package pin.

All report measurements come from the runner. The comparison module is invoked last, after the target firewall is explicitly opened. It cannot feed measured radii, unfolded distances or held-out binding energies back into the solver.

Prior-art credit and official library documentation are in `REFERENCES.md`.
