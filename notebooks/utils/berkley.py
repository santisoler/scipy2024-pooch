import pandas as pd


def preprocess_berkley(df):
    """Pre-process Berkley temperature DataFrame."""
    # Set columns
    columns = [
        "year",
        "month",
        "t_anomaly_monthly",
        "t_anomaly_monthly_uncert",
        "t_anomaly_anually",
        "t_anomaly_anually_uncert",
        "t_anomaly_5y",
        "t_anomaly_5y_uncert",
        "t_anomaly_10y",
        "t_anomaly_10y_uncert",
        "t_anomaly_20y",
        "t_anomaly_20y_uncert",
    ]
    df.columns = columns
    # Add date column and set it as index
    dates = [
        pd.Timestamp(year=year, month=month, day=15)
        for year, month in zip(df.year, df.month)
    ]
    df["date"] = dates
    df = df.set_index("date")
    # Drop year and month
    df = df.drop(columns=["year", "month"])
    # Sort by index
    df = df.sort_index()
    return df
