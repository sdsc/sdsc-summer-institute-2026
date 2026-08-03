# PyPI to Expanse workflow

This is the deployment extension for the 2026 skydiver tutorial. It deliberately
uses a Python package and virtual environment, not Docker, Singularity,
Apptainer, or TSCC.

The workflow has four boundaries:

```text
local source and tests -> published package -> Expanse environment -> scheduled job
```

Each boundary has a different purpose and different credentials. Keep them
separate.

## 1. Prepare a release locally

Work in the root of the student's new repository, not in the large Summer
Institute repository.

Before publishing, make the project metadata unique and accurate:

- In `pyproject.toml`, set `[project].name` to an unused PyPI project name, such
  as `si2026-skydiver-YOUR_GITHUB_USERNAME`.
- Set the author and repository URL to the student's own repository.
- In `skydiver/__init__.py`, set a release version, such as `0.1.0`.
- Each attempted public re-upload requires a **new** version. PyPI will not
  replace a file for an existing project version.

Run the clean local checks:

```bash
python -m pip install --upgrade build twine
nbdev-export
git diff --exit-code
pytest -q
python -m build
python -m twine check dist/*
```

`git diff --exit-code` should be empty. If it is not, the notebook export
changed generated code and that code must be reviewed and committed before the
release.

## 2. Publish without leaking a token

Create a [PyPI account](https://pypi.org/account/register/) and verify its email
address. The manual workshop route is intentionally simple: run Twine locally
and enter `__token__` as the username and a PyPI API token as the password only
when prompted.

```bash
python -m twine upload dist/*
```

Do not paste the token into a command, commit it, add it to a notebook, or copy
it to Expanse. If a local `.env` file is useful for another project, keep it
ignored and document only blank variable names in `.env.example`. Twine does not
load `.env` automatically, so a `.env` file is not required for this tutorial.

### Optional dry run with TestPyPI

TestPyPI is a separate service. It may require its own account and API token.
Upload with:

```bash
python -m twine upload --repository testpypi dist/*
```

When installing from TestPyPI, dependencies such as NumPy still normally come
from PyPI:

```bash
python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  si2026-skydiver-YOUR_GITHUB_USERNAME==0.1.0
```

### Preferred automated release after the workshop

For a GitHub Actions release workflow, use [PyPI Trusted
Publishing](https://docs.pypi.org/trusted-publishers/) instead of keeping a
long-lived PyPI token in GitHub secrets. Configure PyPI to trust the student's
repository and release workflow, then use PyPI's recommended publishing action.
This is an improvement to make after the core tutorial, not a prerequisite for
the 20-minute exercise.

## 3. Install the released package on Expanse

An Expanse account and valid allocation are required. Log in through the
official hostname:

```bash
ssh YOUR_EXPANSE_USERNAME@login.expanse.sdsc.edu
```

Check the projects available to the account:

```bash
module load sdsc
expanse-client user -r expanse
```

For the CPU-only skydiver example, use the CPU software environment. Module
names change, so discover Python before selecting a version:

```bash
module purge
module load cpu
module spider python
# Load one Python module shown by the command above, for example:
# module load python/VERSION_SHOWN_BY_EXPANSE
```

Create one virtual environment in the student's home directory, activate it,
and install the exact package version from PyPI:

```bash
python -m venv ~/venvs/si2026-skydiver
source ~/venvs/si2026-skydiver/bin/activate
python -m pip install --upgrade pip
python -m pip install si2026-skydiver-YOUR_GITHUB_USERNAME==0.1.0
skydiver --mass 80 --drag 0.26
```

The final CLI command is a light installation check. Do not use the login node
for substantive computation. The real tutorial run goes through SLURM.

## 4. Submit the skydiver command through SLURM

Create `run_skydiver.slurm` on Expanse. Replace the account, Python module, and
package version with values that belong to the student.

```bash
#!/bin/bash
#SBATCH --job-name=skydiver
#SBATCH --output=skydiver.%j.out
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --account=YOUR_EXPANSE_ALLOCATION
#SBATCH --no-requeue

set -euo pipefail

module purge
module load cpu
# module load python/VERSION_SHOWN_BY_EXPANSE
source "$HOME/venvs/si2026-skydiver/bin/activate"

skydiver --mass 80 --drag 0.26
```

Submit and monitor it:

```bash
sbatch run_skydiver.slurm
squeue -u "$USER"
```

When the job finishes, inspect the `skydiver.<job-id>.out` file. It should
report terminal velocity near `54.94 m/s downward` and time to 99% near
`14.82 s`.

The `compute` partition and resource values above are intentionally small for
this CPU-only example. For a real model, request the resources the model needs
and follow the current allocation and scheduler guidance.

## Troubleshooting checklist

| Symptom | Likely cause | Next action |
| --- | --- | --- |
| `twine upload` says the file already exists | That project version was already released | Increment `__version__`, rebuild, and upload the new version. |
| PyPI says the project name is unavailable | Another project owns it | Choose a more specific name and update `pyproject.toml`. |
| `pip install` cannot find the package | Upload has not completed, wrong name/version, or TestPyPI was used | Check the project page and use the matching index URL. |
| `module load python` fails | Expanse module names changed | Run `module spider python`, then load an offered version. |
| `sbatch` rejects the account | The account is missing or unauthorized | Use an account listed by `expanse-client user -r expanse`. |
| Package works locally but not in the job | The job did not load the same module or activate the same virtual environment | Put the module and `source .../bin/activate` commands in the SLURM script. |

## Operational references

- [Expanse User Guide](https://www.sdsc.edu/systems/expanse/user_guide.html)
- [PyPI API tokens and account help](https://pypi.org/help/)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)

The user guide is the operational authority for current Expanse access, modules,
partitions, and allocation requirements.
