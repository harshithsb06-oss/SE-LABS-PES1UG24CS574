# Static Analysis Issues

Line numbers below refer to the original `tower_maintenance.py` supplied for Lab 5. Severity is a practical assessment; exact tool codes and severities must be confirmed against the generated reports.

| Issue | Type | Line(s) | Severity | Description | Fix Approach |
|---|---|---:|---|---|---|
| SQL injection risk | Security | 11 | High | The SQL statement is built with string interpolation, so a site name containing SQL syntax can alter the query. | Use SQLite parameter placeholders and pass values as a tuple. |
| Unsafe serialization | Security | 1, 43 | Medium | `pickle` is unnecessary for copying rows and can be dangerous when loading untrusted serialized data. | Return the fetched rows directly as a list; remove `pickle`. |
| Hard-coded credential | Security | 6 | Medium | A password-like secret is embedded in source code and is unused. | Remove the unused secret; load real secrets from a secure configuration source if needed. |
| Broad exception handling | Reliability | 20 | Medium | Catching every `Exception` hides the cause of database errors and can make failures difficult to diagnose. | Catch `sqlite3.Error` and report the error without silently swallowing unrelated exceptions. |
| Missing-row handling | Bug | 35–36 | Medium | `risk_level` can raise `TypeError` when the requested tower ID does not exist because `fetchone()` returns `None`. | Check for a missing row and raise a clear `ValueError`. |
| Naming conventions | Style | 10, 15, 25, 34 | Low | Function names use camelCase instead of Python's snake_case convention. | Rename to `add_tower`, `service_tower`, `overdue_towers`, and `risk_level`. |
| Missing entry-point guard | Maintainability | 54–55 | Low | Calling `main()` at import time runs the demonstration even when another module imports this file. | Use `if __name__ == "__main__":`. |
| Spacing and formatting | Style | 50 | Low | Assignment spacing is inconsistent (`total=len(snapshot())`). | Apply PEP 8 formatting and run Flake8. |
