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

if __name__ == "__main__":
    mcp.run()