import pandas as pd
from main import check_missing, check_duplicates, check_values, check_bounds

def test_check_missing_counts_nulls():
    df = pd.DataFrame({"cost": [100, None, 300]})
    assert check_missing(df, "cost") == 1

def test_check_dupes():
    df = pd.DataFrame({"id": [1, 2, 1], "val": [10, 20, 10]})
    assert check_duplicates(df) == 1

def test_check_values_counts_invalid():
    df = pd.DataFrame({"status": ["active", "frozen", "paused"]})
    assert check_values(df, "status", {"active", "paused", "ended"}) == 1

def test_check_bounds_counts_out_of_range():
    df = pd.DataFrame({"clicks": [50, -5, 2000]})
    assert check_bounds(df, "clicks", 0, 1000) == 2

