import pandas as pd

data = {
    "campaign_id": [101, 102, 103, 101],
    "clicks": [500, 90, -5, 500],
    "cost": [1200, None, 600, 1200],
    "status": ["active", "paused", "frozen", "active"],
}

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

def run_checks(df):
    results = []
    results.append(("missing cost", check_missing(df, "cost")))
    results.append(("duplicate rows", check_duplicates(df)))
    results.append(("invalid status", check_values(df,"status",{"active", "paused", "ended"})))
    results.append(("clicks out of range", check_bounds(df, "clicks", 0, 1000)))
    return results

if __name__ == "__main__":
    #print(check_missing(df, "clicks"))
    #print(check_duplicates(df))
    #print((~df["status"].isin(allowed)).sum())
    #print(check_values(df, "status", {"active", "paused", "ended"}))
    #print(((df["clicks"] < 0) | (df["clicks"] > 1000)).sum())
    #print(check_bounds(df, "clicks", 0, 1000))
    #print(run_checks(df))
    for label, count in run_checks(df):
        status = "PASS" if count == 0 else "FAIL"
        print(f"[{status}] {label}: {count}")