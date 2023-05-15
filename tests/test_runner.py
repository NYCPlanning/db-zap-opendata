import pytest
import pandas as pd
from src.runner import timestamp_to_date

TEST_DATA_PATH = "tests/test_data"

def test_timestamp_to_date():
    data = pd.read_csv(f"{TEST_DATA_PATH}/timestamp_data.csv")
    data_dates = timestamp_to_date(data, date_columns=["date_column_input"])

    assert data_dates["date_column_input"].equals(data_dates["date_column_output"])
