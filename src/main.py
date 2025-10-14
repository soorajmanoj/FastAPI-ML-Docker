# app/main.py

import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
import os

# --- Configuration ---
# The path must be relative to where the script is run.
# We assume the model file is in the root directory relative to 'app/main.py'
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'trained_model.pkl')

try:
    # 1. Load the Model Globally
    # The model loads once when the application starts, not on every request.
    MODEL = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    # In a real-world scenario, you might log this error more formally
    print(f"ERROR: Could not load model from {MODEL_PATH}. Check your path and Stage 1.")
    print(e)
    MODEL = None # Set to None to allow the app to start but fail on predictions

# 2. Initialize the FastAPI application
app = FastAPI(title="Iris ML Predictor Service")

# 3. Define the Input Data Structure (Pydantic Model)
# This ensures that incoming requests have the correct format and data types.
# The Iris dataset uses 4 features, so we define 4 float attributes.
class InputFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# --- API Endpoints ---

@app.get("/")
def home():
    """Basic health check endpoint."""
    return {"message": "ML Service is running. Use /predict to get a prediction."}

@app.post("/predict")
def predict(features: InputFeatures):
    """
    Accepts input features and returns the model prediction.
    """
    if MODEL is None:
        return {"error": "Model failed to load on startup. Cannot predict."}

    # 1. Prepare data for the model
    # Convert Pydantic object to a NumPy array (the format scikit-learn expects)
    data_point = np.array([
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width
    ]).reshape(1, -1) # Reshape into 1 row, 4 columns (1 sample)

    # 2. Make Prediction
    prediction = MODEL.predict(data_point)
    prediction_proba = MODEL.predict_proba(data_point).max()

    # 3. Return Results
    # The Iris model predicts classes (0, 1, or 2).
    return {
        "prediction_class": int(prediction[0]),
        "confidence": round(prediction_proba, 4),
        "input_data": features.model_dump()
    }

# Note: You run this locally using 'uvicorn app.main:app --reload'