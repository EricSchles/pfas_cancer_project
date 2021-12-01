import pandas as pd
import lxml.html
import requests
from scipy.stats import (
    ks_2samp, spearmanr
)
from sklearn.svm import LinearSVR
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

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

def processing_pipeline(all_data, npdes, no_npdes, cancer_df):
    npdes_per_state = npdes["State"].value_counts().reset_index().rename({"index": "State", "State":"npdes_count"}, axis=1)
    no_npdes_per_state = no_npdes["State"].value_counts().reset_index().rename({"index": "State", "State":"no_npdes_count"}, axis=1)
    per_state_count = all_data["State"].value_counts().reset_index().rename({"index": "State", "State":"count"}, axis=1)
    final_df = cancer_df.merge(npdes_per_state, on="State", how="inner")
    final_df = final_df.merge(no_npdes_per_state, on="State", how="inner")
    final_df = final_df.merge(per_state_count, on="State", how="inner")
    
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
    return final_df

# facility name
# lat, lon
# echo id
# industries are different

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

X = final_df[["npdes_count", "count"]]
y = final_df["Rate"]
gbt_reg = GradientBoostingRegressor(learning_rate=0.0001, n_estimators=100000, subsample=0.8, max_depth=4)
gbt_reg.fit(X, y)
y_pred_gbt = gbt_reg.predict(X)
print("fit", mean_absolute_error(y, y_pred_gbt))
print(dict(list(zip(["npdes_count", "count"], gbt_reg.feature_importances_))))
import code
code.interact(local=locals())

#print(ks_2samp(final_df["Rate"], final_df["count"]))
# result: KstestResult(statistic=0.7843137254901961, pvalue=8.916351737215017e-16)
#print(spearmanr(final_df["Rate"], final_df["count"]))
# result: SpearmanrResult(correlation=0.7743891402714933, pvalue=2.6252318611349003e-11)


reg = LinearSVR(random_state=0, tol=1e-5)

    

