import pandas as pd 

from src.features.feature_engineering import azureml_main

def test_temporal_features():
    sample_df = pd.DataFrame({
        "Datetime": ["2002-12-31 01:00:00", "2002-12-31 18:00:00"],
        "PJME_MW": [26498.0, 34017.0]
    })
    (result_df, ) = azureml_main(sample_df)
    expected_cols = ["Hour", "Daysofweek", "Month", "Quarter", "Year", "Dayofyear"]
    for col in expected_cols:
        assert col in result_df.columns, f"Missing expected column: {col}"
        assert result_df[col].isna().sum() == 0, f"Null values found in {col}"

    assert result_df.loc[0, "Hour"] == 1
    assert result_df.loc[1, "Hour"] == 18
    assert result_df.loc[0, "Month"] == 12
    assert result_df.loc[0, "Quarter"] == 4
    assert result_df.loc[0, "Year"] == 2002