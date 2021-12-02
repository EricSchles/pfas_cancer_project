import pandas as pd
import lxml.html
import requests
from mypy import Dict

def read_pfas_data() -> pd.DataFrame:
    return pd.read_excel(
        "Facilities in Industries that May be Handling PFAS Data 07-20-2021.xlsx",
        sheet_name='Data'
    )

def read_cancer_data() -> pd.DataFrame:
    """
    uscs data, data is in rates of incidence per 100,000 people.
    So higher numbers means more cancer incidence in the state, normalized
    for population.
    """
    return pd.read_csv("uscs_map_incidence_all.csv")

def get_us_pop() -> pd.DataFrame:
    return pd.read_csv("2019_Census_US_Population_Data_By_State_Lat_Long.csv")
    
def get_counts_by_state(df: pd.DataFrame, count_col_name: str) -> pd.DataFrame:
    value_counts_per_state = df["State"].value_counts()
    new_dataframe = value_counts_per_state.reset_index()
    return new_dataframe.rename(
        {"index": "State", "State": count_col_name}
        , axis=1
    )

def merge_data(cancer_df, npdes_per_state, no_npdes_per_state, per_state_count):
    final_df = cancer_df.merge(npdes_per_state, on="State", how="inner")
    final_df = final_df.merge(no_npdes_per_state, on="State", how="inner")
    return final_df.merge(per_state_count, on="State", how="inner")

def get_abbreviation_map() -> Dict:
    return {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC",
        "American Samoa": "AS",
        "Guam": "GU",
        "Northern Mariana Islands": "MP",
        "Puerto Rico": "PR",
        "United States Minor Outlying Islands": "UM",
        "U.S. Virgin Islands": "VI",
    }

def transform_state_col(us_pop: pd.DataFrame) -> pd.DataFrame:
    abbreviation_map = get_abbreviation_map()
    us_pop["STATE"] = us_pop["STATE"].map(abbreviation_map)
    return us_pop.rename({"STATE":"State"}, axis=1)

def get_us_population_df() -> pd.DataFrame:
    us_pop = get_us_pop()
    return transform_state_col(us_pop)

def convert_population_for_rate_calculation(final_df):
    # since rate is per 100,000 people, we need to divide the population by 100,000
    final_df["POPESTIMATE2019"] /= 100000
    return final_df

def update_rate_to_total_population(final_df):
    final_df["Rate"] *= final_df["POPESTIMATE2019"]
    return final_df

def processing_pipeline(all_data, npdes, no_npdes, cancer_df):
    npdes_per_state = get_counts_by_state(npdes, "npdes_count")
    no_npdes_per_state = get_counts_by_state(no_npdes, "no_npdes_count")
    per_state_count = get_counts_by_state(all_data, "count")
    final_df = merge_data(
        cancer_df,
        npdes_per_state,
        no_npdes_per_state,
        per_state_count
    )
    us_pop = get_us_population_df()
    final_df = final_df.merge(us_pop, on="State", how="inner")
    final_df = convert_population_for_rate_calculation(final_df)
    return update_rate_to_total_population(final_df)

def main():
    cancer_df = read_cancer_data()
    pfas_generators_df = read_pfas_data()
    pfas_generators_df_npdes = pfas_generators_df[pfas_generators_df["NPDES_FLAG"] == "Y"]
    pfas_generators_df_no_npdes = pfas_generators_df[pfas_generators_df["NPDES_FLAG"] == "N"]
    final_df = processing_pipeline(
        pfas_generators_df,
        pfas_generators_df_npdes,
        pfas_generators_df_no_npdes,
        cancer_df
    )
    final_df.to_csv("state_level_cancer_count_and_pfas_levels.csv")

if __name__ == '__main__':
    main()

    

