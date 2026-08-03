# Session 5.1: Best Practices for Scientific Computing

**SDSC Summer Institute 2026**<br>
**Thursday, August 6, 2026, 8:30-10:00 AM Pacific**<br>
**Presented by Fernando Garzon**

## Session summary

Research often begins in a Jupyter notebook, where exploration is fast but
execution order, hidden state, local files, and one-off environments can make a
successful result difficult to reproduce. This session follows that problem
through modular Python packages, automated tests, GitHub Actions, and a
versioned package that can be installed on Expanse.

The session has three parts:

- **60-minute talk:** notebook failure modes, packages, testing, GitHub
  Actions, and the practical ideas behind MLOps.
- **10-minute Q&A:** questions about applying the workflow to research code.
- **20-minute guided tutorial:** create a clean, independently owned repository
  from the skydiver seed project; test and build it; then follow the documented
  PyPI-to-Expanse deployment path with a facilitator.

The tutorial deliberately does **not** use Docker, Singularity, Apptainer, or
TSCC. Its deployment example is a Python package published to PyPI and
installed on **Expanse**.

## Start here

1. Read the [attendee tutorial](tutorial/README.md).
2. Read the [facilitator guide](tutorial/FACILITATOR.md) before helping a group.
3. Use the detailed [PyPI and Expanse workflow](resources/expanse-pypi-workflow.md)
   for the deployment portion.
4. Open the [PowerPoint](<slides/Architecting reproducible science Best Scientific Computing Practices.pptx>)
   or [PDF](<slides/Architecting reproducible science Best Scientific Computing Practices.pdf>).

## Repository guide

| Path | Purpose |
| --- | --- |
| `tutorial/README.md` | Attendee instructions and the 20-minute core path. |
| `tutorial/FACILITATOR.md` | Preflight checks, timing, expected results, and recovery guidance. |
| `tutorial/skydiver/` | The seed project students copy into a new personal repository. |
| `resources/expanse-pypi-workflow.md` | PyPI publication and Expanse installation/job guidance. |
| `resources/github-actions-test.yml` | CI template for a student repository after the project is copied to its root. |
| `mnist_ae/` | Historical larger packaged-model backup example; it is not the 2026 tutorial path. |
| `slides/` | Final PowerPoint and PDF presentation files. |

## Student repository model

Students should not fork this large Summer Institute repository. Instead, each
student creates a **new, empty GitHub repository**, copies the contents of
`tutorial/skydiver/` into it, and pushes the first commit. That repository is
their own sandbox for GitHub Actions and later releases. The detailed steps,
including `.gitignore`, `.env.example`, and secret handling, are in the
[attendee tutorial](tutorial/README.md).

## What is intentionally not included

Local virtual environments, real `.env` files, PyPI tokens, notebook
checkpoints, build outputs, and raw downloaded MNIST files are excluded. A
template may show variable *names*, but no secret belongs in Git, a notebook,
an issue, a slide, or an Expanse job script.
