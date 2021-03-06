import pandas as pd
import numpy as np
from scipy.stats import (
    ks_2samp, spearmanr
)
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


def get_state_level_cancer_count_and_pfas_levels() -> pd.DataFrame:
    """
    Gets the state level cancer and pfas data which was processed from the
    raw data in data_pipeline.py
    
    Parameters
    ----------
    None

    Returns
    -------
    df : pd.DataFrame - the joined data for Cancer, PFAS and population
    at the state level.
    """
    return pd.read_csv("data/state_level_cancer_count_and_pfas_levels.csv")

def get_Xy(df : pd.DataFrame) -> tuple:
    """
    Splits the data into endogenous and exogenous data.
    
    Parameters
    ----------
    df : pd.DataFrame - the joined data for Cancer, PFAS and population
    at the state level.
    
    Returns
    -------
    * X - the npdes counts and the total facility counts per state
    * y - the rate of cancer incidence per state
    """
    X = df[["npdes_count", "count"]]
    y = df["Rate"]
    return X, y

def get_model() -> GradientBoostingRegressor:
    """
    Generates the model -
    
    The model fails to converge on anything linear,
    implying the data has a highly non-linear relationship.
    The number of estimators is likely around this high,
    however learning rate, regularization and max depth may all
    need to be toyed with further.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The hyper parameters set for a Gradient Boosting Tree.
    """
    return GradientBoostingRegressor(
        learning_rate=0.0001,
        n_estimators=100000,
        subsample=0.8,
        max_depth=4
    )

def get_feature_importances(model) -> dict:
    """
    Gets the feature importances for the regressor.
    
    Parameters
    ----------
    * model : GradientBoostingRegressor - a fit model.
    
    Returns
    -------
    A dictionary of the relative feature importances of:
    * npdes_count
    * count
    
    Note: preliminary results show that npdes is more important than overall count.
    """
    zipped_results = zip(["npdes_count", "count"], model.feature_importances_)
    results = list(zipped_results)
    return dict(results)
    
def get_results(X: pd.DataFrame, y: np.array, model: GradientBoostingRegressor) -> dict:
    """
    This is where the model is trained and the results for analysis
    generated.
    
    The reason we choose not to split into train and test is,
    this model is for _exploratory_ purposes, not for predictive ones.
    There is no "generalization" criteria or intent.  This model is there
    to explain the data, thus there is no reason to split into train and test.
    
    Parameters
    ----------
    * X : pd.DataFrame - the exogenous variables
    * y : np.array - the endogenous variable
    * model : GradientBoostingRegressor - the unfit model

    Returns
    -------
    * fit - mean absolute error for the model
    feature importances for:
    * npdes_count
    * count
    """
    model.fit(X, y)
    y_pred_gbt = model.predict(X)
    feature_importances = get_feature_importances(model)
    model_results = {
        "fit": mean_absolute_error(y, y_pred_gbt),
    }
    model_results.update(feature_importances)
    return model_results

def main():
    df = get_state_level_cancer_count_and_pfas_levels()
    print(ks_2samp(df["Rate"], df["count"]))
    # result: KstestResult(statistic=0.7843137254901961, pvalue=8.916351737215017e-16)
    print(spearmanr(df["Rate"], df["count"]))
    # result: SpearmanrResult(correlation=0.7743891402714933, pvalue=2.6252318611349003e-11)

    X, y = get_Xy(df)
    gbt_reg = get_model()
    results = get_results(X, y, gbt_reg)
    for key_result in results:
        print(key_result, results[key_result])

if __name__ == '__main__':
    main()
