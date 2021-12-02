from scipy.stats import (
    ks_2samp, spearmanr
)
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


X = final_df[["npdes_count", "count"]]
y = final_df["Rate"]
gbt_reg = GradientBoostingRegressor(learning_rate=0.0001, n_estimators=100000, subsample=0.8, max_depth=4)
gbt_reg.fit(X, y)
y_pred_gbt = gbt_reg.predict(X)
print("fit", mean_absolute_error(y, y_pred_gbt))
print(dict(list(zip(["npdes_count", "count"], gbt_reg.feature_importances_))))
