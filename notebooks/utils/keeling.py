import pandas as pd


def preprocess_keeling(df):
    """Pre-process DataFrame containing Keeling curve."""
    import numpy as np

    # Rename columns
    columns = [
        "year",
        "month",
        "excel",
        "decimal_date",
        "co2",
        "co2_no_seasonal",
        "co2_smoothed",
        "co2_smoothed_no_seasonal",
        "co2_filled_missing",
        "co2_no_seasonal_filled_missing",
        "station",
    ]
    df.columns = columns
    # Remove the first two rows
    df = df.drop(index=[0, 1])
    # Cast to numeric values
    for column in set(df.columns) - {"station"}:
        df[column] = pd.to_numeric(df[column])
    # Replace nans
    df = df.replace(-99.99, np.nan)
    # Get dates as Timestamp
    dates = [
        pd.Timestamp(year=year, month=month, day=15)
        for year, month in zip(df.year, df.month)
    ]
    df["date"] = dates
    # Drop columns
    columns_remove = ["year", "month", "excel", "decimal_date"]
    df = df.drop(columns=columns_remove)
    # Reindex
    df = df.set_index("date")
    return df
