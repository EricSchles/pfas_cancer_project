import pandas as pd
from data_pipeline import (
    get_counts_by_state,
    get_abbreviation_map,
    transform_state_col,
    convert_population_for_rate_calculation
)

def test_get_counts_by_state():
    df = pd.DataFrame()
    df = df.append({"State": "NY"}, ignore_index=True)
    counts = get_counts_by_state(df, "count")
    assert counts["count"].iloc[0] == 1

def test_get_abbreviation_map():
    abbreviation_map = get_abbreviation_map()
    assert len(abbreviation_map) == 57

def test_transform_state_col():
    df = pd.DataFrame()
    df = df.append(
        {"STATE": "New York"},
        ignore_index=True
    )
    transformed_df = transform_state_col(df)
    col_list = transformed_df.columns.tolist()
    assert "State" in col_list
    assert "STATE" not in col_list
    assert transformed_df["State"].iloc[0] == "NY"

def test_convert_population_for_rate_calculation():
    df = pd.DataFrame()
    df = df.append(
        {"POPESTIMATE2019": 100000},
        ignore_index=True
    )
    converted_df = convert_population_for_rate_calculation(df)
    assert converted_df["POPESTIMATE2019"].iloc[0] == 1
    
