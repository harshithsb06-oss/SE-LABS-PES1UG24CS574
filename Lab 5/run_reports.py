"""Generate before-and-after reports for the three lab analysis tools."""

from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
TOOLS = {
    "pylint": ["pylint"],
    "bandit": ["bandit", "-r"],
    "flake8": ["flake8"],
}
REPORTS = {"pylint": "pylint_report.txt", "bandit": "bandit_report.txt", "flake8": "flake8_report.txt"}


def run_tool(tool_name, source_file, report_file):
    command = TOOLS[tool_name] + [str(source_file)]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    report_file.write_text(result.stdout + result.stderr, encoding="utf-8")
    print(f"{tool_name}: exit {result.returncode} -> {report_file.relative_to(ROOT)}")


def main():
    missing = [name for name in TOOLS if shutil.which(name) is None]
    if missing:
        raise SystemExit(
            "Missing tools: " + ", ".join(missing)
            + ". Install them with: python -m pip install pylint bandit flake8"
        )

    before_dir = ROOT / "reports" / "before"
    after_dir = ROOT / "reports" / "after"
    before_dir.mkdir(parents=True, exist_ok=True)
    after_dir.mkdir(parents=True, exist_ok=True)

    # The starter source is preserved in the first commit, three commits behind HEAD.
    baseline = subprocess.run(
        ["git", "show", "HEAD~3:tower_maintenance.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    with tempfile.TemporaryDirectory(prefix="tower-analysis-") as temporary:
        before_file = Path(temporary) / "tower_maintenance.py"
        before_file.write_text(baseline, encoding="utf-8")
        for tool_name in TOOLS:
            run_tool(tool_name, before_file, before_dir / REPORTS[tool_name])
            run_tool(tool_name, ROOT / "tower_maintenance.py", after_dir / REPORTS[tool_name])

    print("Reports generated. Review them before committing the report files.")


if __name__ == "__main__":
    main()
