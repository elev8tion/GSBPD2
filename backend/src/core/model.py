import xgboost as xgb
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split

MODEL_PATH = "xgboost_model.pkl"

class PredictionModel:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            print("Model loaded successfully.")
        else:
            print("No model found. Please train the model first.")

    def train(self, df: pd.DataFrame):
        X = df.drop('spread_margin', axis=1)
        y = df['spread_margin']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, max_depth=3)
        self.model.fit(X_train, y_train)
        
        joblib.dump(self.model, MODEL_PATH)
        print("Model trained and saved.")
        return {"status": "success", "message": "Model trained successfully"}

    def predict(self, input_data: dict):
        if not self.model:
            return None, None
        
        df = pd.DataFrame([input_data])
        prediction = self.model.predict(df)[0]
        
        # SHAP Explainability
        try:
            import shap
            explainer = shap.TreeExplainer(self.model)
            shap_values = explainer.shap_values(df)
            # Return the first (and only) row of SHAP values as a dict
            shap_dict = dict(zip(df.columns, shap_values[0]))
        except Exception as e:
            print(f"SHAP Error: {e}")
            shap_dict = {}

        return float(prediction), shap_dict
