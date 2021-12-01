import pandas as pd
import lxml.html
import requests
from scipy.stats import (
    ks_2samp, spearmanr
)


def read_pfas_data():
    return pd.read_excel(
        "Facilities in Industries that May be Handling PFAS Data 07-20-2021.xlsx",
        sheet_name='Data'
    )

def read_cancer_data():
    """
    uscs data, data is in rates of incidence per 100,000 people.
    So higher numbers means more cancer incidence in the state, normalized
    for population.
    """
    return pd.read_csv("uscs_map_incidence_all.csv")

# facility name
# lat, lon
# echo id
# industries are different

cancer_df = read_cancer_data()
pfas_generators_df = read_pfas_data()
pfas_facilities_per_state = pfas_generators_df["State"].value_counts().reset_index().rename({"index": "State", "State":"count"}, axis=1)
final_df = cancer_df.merge(pfas_facilities_per_state, on="State", how="inner")

us_state_to_abbrev = {
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

us_pop = pd.read_csv("2019_Census_US_Population_Data_By_State_Lat_Long.csv")
us_pop["STATE"] = us_pop["STATE"].map(us_state_to_abbrev)
us_pop = us_pop.rename({"STATE":"State"}, axis=1)
final_df = final_df.merge(us_pop, on="State", how="inner")
# since rate is per 100,000 people, we need to divide the population by 100,000
final_df["POPESTIMATE2019"] /= 100000
final_df["Rate"] *= final_df["POPESTIMATE2019"]

print(ks_2samp(final_df["Rate"], final_df["count"]))
# result: KstestResult(statistic=0.7843137254901961, pvalue=8.916351737215017e-16)
print(spearmanr(final_df["Rate"], final_df["count"]))
# result: SpearmanrResult(correlation=0.7743891402714933, pvalue=2.6252318611349003e-11)
    
    

