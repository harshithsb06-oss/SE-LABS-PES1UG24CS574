"""Track telecom tower maintenance using an in-memory SQLite database."""

import sqlite3


CONNECTION = sqlite3.connect(":memory:")
CONNECTION.execute(
    "CREATE TABLE towers ("
    "id INTEGER PRIMARY KEY, site TEXT, last_service INTEGER, faults INTEGER)"
)
service_count = 0


def add_tower(site, last_service, faults=0):
    """Add a tower and its current maintenance details."""
    CONNECTION.execute(
        "INSERT INTO towers (site, last_service, faults) VALUES (?, ?, ?)",
        (site, last_service, faults),
    )
    CONNECTION.commit()


def service_tower(tower_id, year):
    """Record a service visit and reset the tower's fault count."""
    global service_count
    try:
        cursor = CONNECTION.execute(
            "UPDATE towers SET last_service = ?, faults = 0 WHERE id = ?",
            (year, tower_id),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"Tower ID {tower_id} was not found.")
        CONNECTION.commit()
        service_count += 1
    except sqlite3.Error as error:
        CONNECTION.rollback()
        print(f"Service failed: {error}")


def overdue_towers(year):
    """Return site names whose last service was at least two years ago."""
    rows = CONNECTION.execute(
        "SELECT site, last_service FROM towers"
    ).fetchall()
    return [site for site, last_service in rows if year - last_service >= 2]


def risk_level(tower_id):
    """Return a tower's risk category based on its recorded fault count."""
    row = CONNECTION.execute(
        "SELECT faults FROM towers WHERE id = ?", (tower_id,)
    ).fetchone()
    if row is None:
        raise ValueError(f"Tower ID {tower_id} was not found.")
    return "high" if row[0] > 3 else "normal"


def snapshot():
    """Return a snapshot of all tower records."""
    return CONNECTION.execute("SELECT * FROM towers").fetchall()


def main():
    """Run a short demonstration of the maintenance tracker."""
    add_tower("Ridge-A", 2021, 5)
    add_tower("Coast-B", 2024)
    service_tower(2, 2025)
    total = len(snapshot())
    print(overdue_towers(2025), risk_level(1), total, service_count)


if __name__ == "__main__":
    main()