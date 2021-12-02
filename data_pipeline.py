import pandas as pd

def read_pfas_data() -> pd.DataFrame:
    """
    https://echo.epa.gov/ is the source for this data.

    Parameters
    ----------
    None
    
    Returns
    -------
    Passes back all known PFAS facilities as of 7/20/2021 as a dataframe.
    """
    return pd.read_excel(
        "data/Facilities in Industries that May be Handling PFAS Data 07-20-2021.xlsx",
        sheet_name='Data'
    )

def read_cancer_data() -> pd.DataFrame:
    """
    
    https://statecancerprofiles.cancer.gov/ is the source for this data.
    
    Note:
    uscs data, data is in rates of incidence per 100,000 people.
    So higher numbers means more cancer incidence in the state, normalized
    for population.

    Parameters
    ----------
    None
    
    Returns
    -------
    Passes back all known cancer incidence for 2013 as a dataframe.
    """
    return pd.read_csv("data/uscs_map_incidence_all.csv")

def get_us_pop() -> pd.DataFrame:
    """
    https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html is 
    the source for this data.

    Parameters
    ----------
    None

    Returns
    -------
    Passes back 2019 census data at the state level as a dataframe.
    """
    return pd.read_csv("data/2019_Census_US_Population_Data_By_State_Lat_Long.csv")
    
def get_counts_by_state(df: pd.DataFrame, count_col_name: str) -> pd.DataFrame:
    """
    Counts the number of PFAS facilities per state and saves the results
    as a dataframe.

    Parameters
    ----------
    * df : pd.DataFrame - A dataframe of PFAS facilities, which
    may or may not be filtered on one or more fields.
    * count_col_name : str - the name of the count, since we are
    filtering on multiple fields.
    
    Returns
    -------
    The count of PFAS facilities, potentially subject to a filter.
    """
    value_counts_per_state = df["State"].value_counts()
    new_dataframe = value_counts_per_state.reset_index()
    return new_dataframe.rename(
        {"index": "State", "State": count_col_name}
        , axis=1
    )

def merge_data(
        cancer_df: pd.DataFrame,
        npdes_per_state : pd.DataFrame,
        no_npdes_per_state : pd.DataFrame,
        per_state_count : pd.DataFrame) -> pd.DataFrame:
    """
    Merges all PFAS count dataframes with the cancer data, at the state level.
    
    Parameters
    ----------
    * cancer_df : pd.DataFrame - the cancer data from uscs
    * npdes_per_state : pd.DataFrame - data with the npdes code set to yes,
    npdes means PFAS is potentially dumped in the water ways
    * no_npdes_per_state : pd.DataFrame - data with code set to no,
    this means PFAS was not dumped in the water at this facility, probably.
    * per_state_count : pd.DataFrame - the total count of all PFAS generating
    facilities at the state level.

    Returns
    -------
    A merged dataframe of cancer and pfas facility counts at the state level.
    """
    final_df = cancer_df.merge(npdes_per_state, on="State", how="inner")
    final_df = final_df.merge(no_npdes_per_state, on="State", how="inner")
    return final_df.merge(per_state_count, on="State", how="inner")

def get_abbreviation_map() -> dict:
    """
    This is a dictionary with the full state names, upper cased
    to their two letter abbreviation.
    
    Parameters
    ----------
    None

    Returns
    -------
    A dictionary or 'map' of full state names to 
    two letter abbreviations.
    """
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
    """
    Standardizes the 'STATE' column and abbreviates all states
    to two letter form.
    
    Parameters
    ----------
    * us_pop : pd.DataFrame - the approximate populations for all
    50 states.
    
    Returns
    -------
    A version of the us population dataframe with the states
    normalized to interoperate with the other dataframes, which
    use the two letter abbreviation for state names.
    """
    abbreviation_map = get_abbreviation_map()
    us_pop["STATE"] = us_pop["STATE"].map(abbreviation_map)
    return us_pop.rename({"STATE":"State"}, axis=1)

def get_us_population_df() -> pd.DataFrame:
    """
    Gets and transforms the us population data.
    
    Parameters
    ----------
    None
    
    Returns
    --------
    US population data with normalized 'State' column.
    """
    us_pop = get_us_pop()
    return transform_state_col(us_pop)

def convert_population_for_rate_calculation(final_df : pd.DataFrame) -> pd.DataFrame:
    """
    Converts population for the rate calculation
    from the uscs cancer data.

    Note: since rate is per 100,000 people, 
    we need to divide the population by 100,000
    
    Parameters
    ----------
    * final_df : pd.DataFrame - the combination
    of cancer, PFAS and population data.
    
    Returns
    -------
    Returns the population estimate from the census data
    divided by 100,000 to deal with the Rate variable being 
    'Rate per 100,000 people'.
    """
    final_df["POPESTIMATE2019"] /= 100000
    return final_df

def update_rate_to_total_population(final_df : pd.DataFrame) -> pd.DataFrame:
    """
    For some reason the cancer rate is reported per 100,000 people by uscs.
    I could not find any cancer rates in raw numbers anywhere.  So this
    function converts the cancer data back to total rate of incidence per
    year.
    
    Parameters
    ----------
    * final_df : pd.DataFrame - the joined data for Cancer, PFAS and population
    at the state level.
    
    Returns
    -------
    The same data, with the rate in total population per year per state
    rather than per 100,000 people.
    """
    final_df["Rate"] *= final_df["POPESTIMATE2019"]
    return final_df

def processing_pipeline(
        all_data: pd.DataFrame,
        npdes: pd.DataFrame,
        no_npdes : pd.DataFrame ,
        cancer_df : pd.DataFrame) -> pd.DataFrame:
    """
    This the full processing pipeline for all the all the factors:
    * Census data
    * PFAS facility counts per state
    * Rate of Cancer incidence per state
    
    Parameters
    ----------
    * all_data : pd.DataFrame - counts for all pfas facilities.
    * npdes : pd.DataFrame - counts for all npdes pfas facilities 
    (those that dump in the water).
    * no_npdes : pd.DataFrame - counts for all facilities not designated
    npdes pfas. Those that don't dump in the water.
    * cancer_df : pd.DataFrame - the rate of cancer incidence per state.

    Returns
    -------
    final_df : pd.DataFrame - the joined data for Cancer, PFAS and population
    at the state level.
    """
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
    pfas_generators_df = read_pfas_data()
    cancer_df = read_cancer_data()
    pfas_generators_df_npdes = pfas_generators_df[pfas_generators_df["NPDES_FLAG"] == "Y"]
    pfas_generators_df_no_npdes = pfas_generators_df[pfas_generators_df["NPDES_FLAG"] == "N"]
    final_df = processing_pipeline(
        pfas_generators_df,
        pfas_generators_df_npdes,
        pfas_generators_df_no_npdes,
        cancer_df
    )
    final_df.to_csv("data/state_level_cancer_count_and_pfas_levels.csv")

if __name__ == '__main__':
    main()

    

