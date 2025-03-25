import pickle
import numpy as np
import pandas as pd
import xgboost as xgb
from flask import Flask, render_template, request

# Load the trained model
model = xgb.Booster()
model.load_model("updated_model.model")

# Load preprocessing files
with open("scaler2.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

with open("selected_featuresfinal.pkl", "rb") as feature_file:
    selected_features = pickle.load(feature_file)

with open("label_encodersfinal.pkl", "rb") as le_file:
    label_encoders = pickle.load(le_file)

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template("index.html")

# Prediction Route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect form data
        input_data = {key: request.form[key] for key in request.form}

        # Convert to DataFrame
        df = pd.DataFrame([input_data])

        # Convert categorical features using label encoders
        for col, le in label_encoders.items():
            if col in df.columns:
                df[col] = df[col].map(lambda s: le.transform([s])[0] if s in le.classes_ else -1)

        # Convert numeric columns properly
        numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Select only the required features
        df = df[selected_features]

        # Apply scaling
        df_scaled = scaler.transform(df)

        # Convert to DMatrix with feature names
        dmatrix = xgb.DMatrix(df_scaled, feature_names=selected_features)

        # Make prediction
        prediction = model.predict(dmatrix)[0]
        churn_result = "Yes" if prediction > 0.5 else "No"

        return render_template("index.html", prediction=churn_result, probability=round(float(prediction), 4))

    except Exception as e:
        return render_template("index.html", error=str(e))
 
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
