# Lab 5: Static Code Analysis — Telecom Tower Maintenance Tracker

**Forked repository:** https://github.com/harshithsb06-oss/L5_25_tower_maintenance

## Program

A small SQLite-backed tracker that logs towers and faults, records servicing, lists overdue towers, and rates tower risk.

## Setup and run

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install pylint bandit flake8
python tower_maintenance.py
```

## Static analysis reports

Install the tools, then generate all six reports (before and after) with:

```bash
python run_reports.py
```

The script runs the tools against the starter source preserved in Git history and the final source. It writes reports to `reports/before/` and `reports/after/`. Review the outputs and commit them before submission. The reports are not prefilled with invented tool results.
See [`issues.md`](issues.md) for the issue table and [`reflection.md`](reflection.md) for the lab reflection.

## Commit plan

The history contains three issue-fix commits after the starter snapshot:

1. Security: parameterized SQL, removed `pickle` round-trip and embedded unused credential.
2. Style: converted function names to snake_case and corrected formatting.
3. Reliability/maintainability: narrowed database exception handling, handled missing tower IDs, added docstrings and a main guard.

The assignment requires three commits for the tool-related fixes. The starter snapshot is an additional baseline commit used to make the before/after history auditable.
