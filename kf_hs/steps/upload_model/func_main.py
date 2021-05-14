import joblib
import numpy as np

# Load a model once
model = joblib.load("/model/files/model.joblib")

def infer(x1, x2):
    # Make a prediction
    y = model.predict([[x1, x2]])
    # Return the scalar representation of y
    return {"y": y.item()}