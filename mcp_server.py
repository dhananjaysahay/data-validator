from mcp.server.fastmcp import FastMCP
from sqlalchemy import create_engine, inspect
import pandas as pd
from main import run_checks, rules

mcp = FastMCP("data-quality")
engine = create_engine("sqlite:////Users/dhananjaysahay/code/data-validator/campaigns.db")

@mcp.tool()
def list_tables() -> list[str]:
    """List all tables in the campaigns database."""
    return inspect(engine).get_table_names()

@mcp.tool()
def run_quality_checks(table: str) -> list:
    """Run all configured data-quality checks on table and return(label, count) results."""
    df = pd.read_sql(f"SELECT * FROM {table}", engine)
    return run_checks(df,rules)

@mcp.tool()
def get_failing_rows(table: str, check: str) -> list:
    """Return the actual rows that fail a given check. Use this after
    run_quality_checks reports a non-zero count. The check argument is the
    check's label, for example 'missing cost' or 'duplicate rows'."""
    df = pd.read_sql(f"SELECT * FROM {table}", engine)
    for rule in rules:
        if rule["label"] == check:
            if rule["check"] == "missing":
                mask = df[rule["column"]].isnull()
            elif rule["check"] == "duplicates":
                mask = df.duplicated()
            elif rule["check"] == "values":
                mask = ~df[rule["column"]].isin(rule["allowed"])
            elif rule["check"] == "bounds":
                mask = (df[rule["column"]] < rule["low"]) | (df[rule["column"]] > rule["high"])
            return df[mask].to_dict(orient="records")
    return []

if __name__ == "__main__":
    mcp.run()