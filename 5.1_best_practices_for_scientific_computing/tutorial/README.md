# Twenty-minute tutorial: own the package, then run it on Expanse

This tutorial uses the small skydiving model to show a realistic path from
notebook code to a package another machine can install. You will create a new
personal GitHub repository, copy the seed project into it, run its tests, and
build a package. Publishing to PyPI and installing on Expanse are documented
next steps that the facilitator can guide after the core exercise.

The goal is not to finish every account setup in twenty minutes. The goal is to
leave with a repository you own and a clear, safe deployment path.

## Before the session

Bring a GitHub account. If you plan to publish during or after the tutorial,
also create a [PyPI account](https://pypi.org/account/register/) and verify its
email address. A separate [TestPyPI](https://test.pypi.org/account/register/)
account is optional but useful for a dry run.

An Expanse login and a valid allocation are needed only for the final install
and SLURM job. Do not block the core tutorial waiting for either one.

## 0-4 minutes: create your own repository

1. On GitHub, create a **new empty repository** named something like
   `si2026-skydiver-yourname`.
2. Do **not** fork the Summer Institute repository. A new repository lets your
   own GitHub Actions workflow run without the permissions and policy limits of
   the course repository.
3. Clone your empty repository locally.

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/si2026-skydiver-yourname.git
cd si2026-skydiver-yourname
```

Copy the contents of this repository's `tutorial/skydiver/` directory into the
new clone. Use your file browser or an equivalent copy command. Copy source,
notebook, tests, `pyproject.toml`, and `README.md`; do not intentionally copy a
virtual environment, `.pytest_cache`, `build/`, `dist/`, or `*.egg-info`.

The copied project is a starting point, not a fork. Your Git history begins in
your own repository.

## 4-7 minutes: protect local configuration and secrets

Create a `.gitignore` at the root of your new repository:

```gitignore
# Local configuration and secrets
.env
.env.*
!.env.example

# Python environments and generated files
.venv/
venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ipynb_checkpoints/

# Package build artifacts
build/
dist/
*.egg-info/
```

Commit a safe `.env.example` only when your project actually needs configurable
values. It documents variable names, never values:

```dotenv
# Example only. Leave real secrets out of this file.
# PYPI_API_TOKEN=
```

For this tutorial, a PyPI token is only used to upload from your own computer.
It is **not** needed on Expanse and must never be committed. A `.env` file is
not automatically read by Python, Twine, or SLURM; it is merely a local
convention. The safest workshop option is to let Twine prompt for the token.

## 7-12 minutes: install, export, and test

Create and activate a local virtual environment, then install the copied
project and its development tools:

```bash
python -m venv .venv

# macOS or Linux
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
nbdev-export
pytest -q
```

The tests protect scientific behavior: a known terminal velocity, the approach
to terminal velocity, and invalid physical parameters. The source notebook
remains useful for exploration, while `skydiver/physics.py` is the reusable,
importable package code.

## 12-15 minutes: make the package yours

Open `pyproject.toml` and make these changes before any public upload:

- Choose a unique project name, for example
  `si2026-skydiver-YOUR_GITHUB_USERNAME`.
- Update the author and repository URL.
- Keep the package import name (`skydiver`) unless you deliberately rename it
  everywhere.
- Confirm the release version in `skydiver/__init__.py`. PyPI never allows the
  same project version to be uploaded twice.

Then build and validate the distribution:

```bash
python -m build
python -m twine check dist/*
```

## 15-20 minutes: commit and enable CI

Make the first commit in your own repository:

```bash
git add .
git status
git commit -m "Start skydiver package"
git push -u origin main
```

Create `.github/workflows/test.yml` in your new repository using the workflow
shown in [GitHub Actions for the copied project](#github-actions-for-the-copied-project).
Commit and push it. Open the **Actions** tab in your own repository and confirm
that the test-and-build workflow starts.

If account setup or package naming takes longer, stop here. You have completed
the essential exercise. Continue with the facilitator using the
[PyPI and Expanse workflow](../resources/expanse-pypi-workflow.md).

## Publish and run after the core exercise

Use the detailed workflow for the remaining steps:

1. Upload a uniquely named, versioned wheel to TestPyPI or PyPI.
2. Log in to Expanse.
3. Create a virtual environment there and install your exact released package.
4. Submit the CPU-only skydiver command through SLURM.

Do not upload a PyPI token to GitHub Actions. For automated releases, configure
[PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) after the
workshop instead of storing a long-lived token in GitHub.

## GitHub Actions for the copied project

The file `resources/github-actions-test.yml` is a template for the older nested
course-repository layout. In your own repository the copied package lives at
the repository root, so use this root-level workflow instead:

```yaml
name: Test and build

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: python -m pip install -e ".[dev]"
      - run: nbdev-export
      - run: git diff --exit-code
      - run: pytest -q
      - run: python -m build
```

The `git diff --exit-code` step catches a common nbdev mistake: changing an
exported notebook cell but forgetting to commit the generated Python module.
