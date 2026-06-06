import pandas as pd

data = {
    "campaign_id": [101, 102, 103, 101],
    "clicks": [500, 90, -5, 500],
    "cost": [1200, None, 600, 1200],
    "status": ["active", "paused", "frozen", "active"],
}

rules = [
    {"check": "missing", "column": "clicks", "label": "missing clicks"},
    {"check": "missing", "column": "cost", "label": "missing cost"},
    {"check": "duplicates", "label": "duplicate rows"},
    {"check": "values", "column": "status", "allowed": {"active", "paused", "ended"}, "label": "invalid status"},
    {"check": "bounds", "column": "clicks", "low": 0, "high": 1000, "label": "clicks out of range"},
]

df = pd.DataFrame(data)

allowed = {"active", "paused", "ended"}

def check_missing(df: pd.DataFrame, column: str) -> int:
    return int(df[column].isnull().sum())

def check_duplicates(df: pd.DataFrame) -> int:
    return int(df.duplicated().sum())

def check_values(df: pd.DataFrame, column: str, allowed: set) -> int:
    return int((~df[column].isin(allowed)).sum())

def check_bounds(df: pd.DataFrame, column: str, low: int, high: int) -> int:
    return int(((df[column] < low) | (df[column] > high)).sum())

def run_checks(df, rules):
    results = []
    for rule in rules:
        if rule["check"] == "missing":
            count = check_missing(df, rule["column"])
        elif rule["check"] == "duplicates":
            count = check_duplicates(df)
        elif rule["check"] == "values":
            count = check_values(df, rule["column"], rule["allowed"])
        elif rule["check"] == "bounds":
            count = check_bounds(df, rule["column"], rule["low"], rule["high"])
        results.append((rule["label"],count))
    return results

if __name__ == "__main__":
    #print(check_missing(df, "clicks"))
    #print(check_duplicates(df))
    #print((~df["status"].isin(allowed)).sum())
    #print(check_values(df, "status", {"active", "paused", "ended"}))
    #print(((df["clicks"] < 0) | (df["clicks"] > 1000)).sum())
    #print(check_bounds(df, "clicks", 0, 1000))
    #print(run_checks(df))
    for label, count in run_checks(df, rules):
        status = "PASS" if count == 0 else "FAIL"
        print(f"[{status}] {label}: {count}")