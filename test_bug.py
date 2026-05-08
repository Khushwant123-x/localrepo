from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import StackingRegressor
from xgboost import XGBRegressor

model = MultiOutputRegressor(
    StackingRegressor(
        estimators=[("xgb", XGBRegressor())],
        final_estimator=XGBRegressor()
    )
)

print("SUCCESS")