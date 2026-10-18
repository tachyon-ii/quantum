# Sources and credit
<!-- Implementer: OpenAI ChatGPT — GPT-6 Astra Pro -->

## Physics source

`BUILD-SPEC-membrane-solver.md`, supplied by the user, is the sole source of physical constants, functionals, starting configurations, calibration data, prediction targets and requested acceptance tests.

The companion physics documents mentioned by the build were not supplied. Their contents are not inferred or used as additional input.

## Prior art explicitly credited in the build

Seifert & Lipowsky (1990): vesicle adhesion with a contact potential.

Kendall (1971): peel mechanics.

Helfrich (1973): bending energy.

These credits identify the antecedents requested in the build. No additional formula, contact factor, stiffness, or empirical target has been imported from those works. No Timoshenko term is used.

## Official implementation documentation

SciPy L-BFGS-B options, including projected-gradient termination, independent energy-change termination, and iteration/evaluation limits:

https://docs.scipy.org/doc/scipy/reference/optimize.minimize-lbfgsb.html

SciPy cKDTree exact neighbourhood query:

https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.query_ball_point.html

PyTorch autograd gradients, matching the installed major/minor release:

https://docs.pytorch.org/docs/2.10/generated/torch.autograd.grad.html

These documentation sources were consulted for API semantics, not as extra physics inputs. The actual tested dependency versions are recorded by the runner and pinned in `requirements.txt`.
