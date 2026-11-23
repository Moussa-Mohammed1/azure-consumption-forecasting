import pandas as pd

def azureml_main(dataframe1=None, dataframe2=None):
    """
    Entry point required by Azure ML Designer's 'Execute Python Script' module.
    Extracts temporal features from the 'Datetime' column.
    """
    if dataframe1 is None:
        raise ValueError("Input dataframe1 cannot be None.")

    df = dataframe1.copy()

    df["Datetime"] = pd.to_datetime(df["Datetime"])

    df["Hour"] = df["Datetime"].dt.hour
    df["Daysofweek"] = df["Datetime"].dt.dayofweek
    df["Month"] = df["Datetime"].dt.month
    df["Quarter"] = df["Datetime"].dt.quarter
    df["Year"] = df["Datetime"].dt.year
    df["Dayofyear"] = df["Datetime"].dt.dayofyear

    return (df,)
