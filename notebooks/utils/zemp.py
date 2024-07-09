def preprocess_zemp(df):
    """Pre-process glacier mass balance DataFrame."""
    df.columns = [c.strip() for c in df.columns]
    df = df.set_index("Year")
    return df
