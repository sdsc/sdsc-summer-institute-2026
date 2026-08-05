# Deployment resources

This folder contains the two supporting resources used by the current tutorial.
It is deliberately small: the lesson publishes a Python package to PyPI and
installs it in a virtual environment on Expanse. It does not use containers or
TSCC.

| File | Purpose |
| --- | --- |
| `expanse-pypi-workflow.md` | Step-by-step guide from a tested wheel to PyPI, an Expanse virtual environment, and a small CPU SLURM job. |
| `github-actions-test.yml` | Test-and-build workflow template; `tutorial/README.md` explains the small path adjustment needed after students copy the project into their own repository. |

For current operational details such as Expanse modules, allocation names, and
partitions, use the [Expanse User Guide](https://www.sdsc.edu/systems/expanse/user_guide.html).
