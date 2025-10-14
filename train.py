import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import os

print("Starting model training...")

# 1. Load Data
X, y = load_iris(return_X_y=True)

# 2. Train Model (Using a simple Logistic Regression)
clf = LogisticRegression(max_iter=200)
clf.fit(X, y)

print("Model trained successfully.")

# 3. Define Save Path
# Ensure the model directory exists
MODEL_DIR = "model"
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

MODEL_PATH = os.path.join(MODEL_DIR, "trained_model.pkl")

# 4. Save the Trained Model
# joblib is generally preferred over pickle for large numpy objects often found in scikit-learn
joblib.dump(clf, MODEL_PATH)

print(f"Model saved to: {MODEL_PATH}")
print("Stage 1 complete!")