# Lab 5 Reflection

## 1. What is static code analysis, and why is it useful?
Static code analysis examines source code without running the program. It helps identify likely bugs, insecure patterns, maintainability problems, and style violations early, before they reach production.

## 2. What are the differences between Pylint, Bandit, and Flake8?
Pylint checks broad code quality, design, naming, and likely programming errors. Bandit focuses on common Python security risks. Flake8 checks style and common lint errors, including many PEP 8 formatting violations. Their findings overlap in places, but their primary purposes differ.

## 3. Which issues were identified and how were they fixed?
The original program interpolated a site name directly into SQL, used `pickle` for an unnecessary copy, contained an unused hard-coded password-like value, caught overly broad exceptions, and did not handle an unknown tower ID in the risk lookup. The SQL operation was parameterized, the pickle round-trip and unused secret were removed, exception handling was narrowed, and missing tower IDs now produce a clear error. Function names and formatting were also improved.

## 4. How did static analysis improve the program, and what are its limitations?
Static analysis makes recurring problems visible and provides a repeatable way to check code after changes. It does not prove the program is correct, replace tests, or catch every runtime or business-logic defect. Findings need to be reviewed, fixes need to preserve behavior, and the tools must be rerun to verify the result. The Pylint, Bandit, and Flake8 reports and final Pylint score should be generated locally after installing the tools; this environment could not access the package index, so no tool output or score is claimed here.
