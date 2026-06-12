# Data Validation Tool

A modular Python validator that pulls operational data from a SQL database and runs configurable rule checks — nulls, duplicates, value-set membership, and numeric bounds — outputting a structured pass/fail report.

```
[PASS] missing clicks: 0
[FAIL] missing cost: 1
[FAIL] duplicate rows: 1
[FAIL] invalid status: 1
[FAIL] clicks out of range: 1
```

## How it works

## MCP server

The validator is also exposed as an MCP (Model Context Protocol) server, so AI
clients like Claude Desktop can run data-quality checks conversationally —
"is my campaigns table healthy?" becomes a tool call against this code.

Tools exposed:

- `list_tables()` — list the tables in the database
- `run_quality_checks(table)` — run all configured checks, return `(label, count)` results
- `get_failing_rows(table, check)` — return the actual rows failing a given check

To use it, point your MCP client at `mcp_server.py`, launched with this
project's venv Python (see `claude_desktop_config.json` docs for Claude Desktop).

```
SQL database → read into a DataFrame → run_checks() over a rules list → PASS/FAIL report
```

The defining feature is that checks are **configuration, not code**. They live in a plain list of dicts:

```python
rules = [
    {"check": "missing", "column": "cost", "label": "missing cost"},
    {"check": "duplicates", "label": "duplicate rows"},
    {"check": "values", "column": "status",
     "allowed": {"active", "paused", "ended"}, "label": "invalid status"},
    {"check": "bounds", "column": "clicks", "low": 0, "high": 1000,
     "label": "clicks out of range"},
]
```

A generic `run_checks()` engine reads the list and dispatches to the matching check. Adding a new check is one line of data — the engine never changes.

Every check shares one mechanical shape: **build a boolean mask where `True` marks a violation, then `.sum()` it** (True counts as 1):

| Check | Mechanism |
|---|---|
| `check_missing` | `df[col].isnull().sum()` |
| `check_duplicates` | `df.duplicated().sum()` |
| `check_values` | `(~df[col].isin(allowed)).sum()` |
| `check_bounds` | `((df[col] < low) \| (df[col] > high)).sum()` |

Data flows through a real SQL layer: the table is written to SQLite via SQLAlchemy (`to_sql`), read back with `read_sql`, and the validator runs on the database-sourced DataFrame. Swapping SQLite for Postgres/MySQL is a connection-string change — the rest of the code is identical.

## Running it

```bash
git clone https://github.com/dhananjaysahay/data-validator.git
cd data-validator
python3 -m venv .venv && source .venv/bin/activate
pip install pandas sqlalchemy pytest
python main.py   # seeds campaigns.db, validates it, prints the report
pytest           # run the check tests
```

## Design decisions

- **Checks return counts, not booleans.** A count carries magnitude ("3 problems"); pass/fail is trivially derived from `count == 0`. A boolean throws information away.
- **Config-driven rules.** Separating *what to check* (data) from *how to check* (engine) means extending behavior without touching — or risking — working logic.
- **Runtime behind `main()`.** Python executes top-level code on import. Wrapping the database work in `main()` under `if __name__ == "__main__":` means tests can import the check functions without side effects.
- **`int()` at the boundary.** pandas' `.sum()` returns `numpy.int64`, which won't serialize to JSON and prints as `np.int64(1)` inside containers. Each check casts to a native int.

## Testing

One test per check, each building a tiny DataFrame with a known number of violations and asserting the exact count. The bounds test deliberately breaks both the low and high bound to prove both halves of the `|` work.
