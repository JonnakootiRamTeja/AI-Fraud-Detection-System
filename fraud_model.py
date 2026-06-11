import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Dummy dataset (you can later replace with real dataset)
data = {
    "amount": [100, 5000, 200, 10000, 300],
    "location": [1, 5, 1, 10, 2],
    "is_fraud": [0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

X = df[["amount", "location"]]
y = df["is_fraud"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "fraud_model.pkl")