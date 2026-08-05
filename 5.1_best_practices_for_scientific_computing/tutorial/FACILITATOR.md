# Facilitator guide: skydiver package to PyPI and Expanse

This guide supports the final 20 minutes of the session. The presenter has
already completed the 60-minute talk and 10-minute Q&A. Your job is to keep the
room moving, not to make every student finish PyPI registration or log into
Expanse in real time.

## The outcome to protect

The minimum successful outcome is that each participant has:

1. a new repository they own, rather than a fork of the course repository;
2. the skydiver seed project copied into that repository;
3. a `.gitignore` that excludes `.env`, virtual environments, and build output;
4. a passing local test run and a built distribution; and
5. a clear next-step document for publication and Expanse.

Publishing to PyPI and submitting an Expanse job are the extension path. They
are valuable demonstrations, but should never hold up the rest of the room.

## Before the session

On the instructor machine, verify the seed project from
`tutorial/skydiver/`:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
nbdev-export
pytest -q
python -m build
python -m twine check dist/*
python -m skydiver.cli --mass 80 --drag 0.26
```

On Windows, activate with `.\.venv\Scripts\Activate.ps1`.

Expected results:

- all tests pass;
- `twine check` succeeds;
- the CLI reports about `54.94 m/s` downward and `14.82 s` to reach 99% of
  terminal velocity.

Before class, have these ready:

- the repository URL and local path to the seed project;
- a screen showing how to create a new empty GitHub repository;
- the current [Expanse User Guide](https://www.sdsc.edu/systems/expanse/user_guide.html);
- one instructor-owned package already published to PyPI, in case students are
  still completing PyPI account verification; and
- one tested Expanse CPU job script and its resulting output file, in case the
  scheduler queue is slow.

Never ask students to share a PyPI token, password, SSH private key, one-time
code, or allocation credentials on screen, in chat, or in a repository.

## Suggested pacing

| Time | Facilitation cue | Recovery rule |
| --- | --- | --- |
| 0-4 min | Have everyone create and clone a new empty repository. Explain why this is not a fork. | Pair students who are still creating GitHub accounts; do not wait for them. |
| 4-7 min | Copy `tutorial/skydiver/` and add `.gitignore` plus a harmless `.env.example`. | If copying is slow, provide a prepared ZIP or let the student follow your screen. |
| 7-12 min | Create a virtual environment; run `nbdev-export` and `pytest -q`. | The generated `skydiver/physics.py` is already committed, so a student can continue even if nbdev fails. |
| 12-15 min | Change project metadata and build with `python -m build`. | Do not publish under the shared default name. Use a unique name first. |
| 15-20 min | Push the personal repository and add the root-level Actions workflow. | If Actions has not finished, show the workflow on your prepared repository. |
| After core | Guide interested students through PyPI and Expanse using `../resources/expanse-pypi-workflow.md`. | Demonstrate with the instructor package if accounts, email verification, or the queue delay a student. |

## Explaining the two credentials

Students often conflate three different things. Keep the distinction explicit:

| Credential | Where it belongs | What it does |
| --- | --- | --- |
| GitHub authentication | Git credential manager, SSH key, or GitHub CLI | Pushes to the student's own repository. |
| PyPI API token | Entered locally when Twine prompts, or replaced by Trusted Publishing | Uploads a release. It is never needed on Expanse. |
| Expanse login and allocation | SDSC/ACCESS login plus the student's authorized account in a SLURM script | Installs/runs the already-published package. |

`.env` is a local configuration convention, not a secret vault and not a
deployment mechanism. The project `.gitignore` must exclude it. A committed
`.env.example` may list variable names with blank values, but the tutorial does
not need to load a `.env` file at all.

## PyPI help

Use this decision tree:

- **No PyPI account or email is unverified:** finish the repository, build, and
  CI steps; use the prepared instructor package for the Expanse demonstration.
- **Package name already exists:** change `[project].name` in `pyproject.toml`.
  A name containing the student's GitHub username is usually sufficient.
- **"File already exists" during upload:** bump `__version__` in
  `skydiver/__init__.py`, rebuild, and upload the new version. PyPI releases are
  immutable.
- **Student wants a dry run:** use TestPyPI. It is a different service and may
  require a separate account/token.
- **Student asks where to put a token:** do not put it in Git, GitHub Actions,
  an `.env.example`, or Expanse. Let Twine prompt locally, or later configure
  PyPI Trusted Publishing for their own repository.

The complete commands and explanations are in
[`../resources/expanse-pypi-workflow.md`](../resources/expanse-pypi-workflow.md).

## Expanse help

The skydiver example is CPU-only. The correct lesson is package portability,
not GPU usage. Have students:

1. use `expanse-client user -r expanse` to identify an authorized account;
2. load the CPU environment and an available Python module;
3. create a virtual environment outside the source repository;
4. install the exact package and version from PyPI; and
5. submit the CLI through the `compute` partition with a small resource request.

If `module load python` fails, use `module spider python` and load a version
shown by Expanse. Do not guess a module name. If `sbatch` rejects an account,
the student must use an account returned by `expanse-client`; do not borrow
another student's allocation.

The login node is for editing, setup, and light checks. The actual CLI run in
the tutorial should be submitted as a small SLURM job, as shown in the workflow
guide.

## Discussion prompt

Ask: "Which assumption in your own research code deserves a test before you run
it for hours on Expanse?"
