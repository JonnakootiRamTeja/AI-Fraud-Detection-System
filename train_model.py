import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib


df = pd.read_csv("creditcard.csv")
X = df.drop("Class", axis=1)
y = df["Class"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
pred = model.predict(X_test)
accuracy = accuracy_score(y_test, pred)
print("Model Accuracy:", accuracy)
cm = confusion_matrix(y_test, pred)

print("Confusion Matrix")
print(cm)
joblib.dump(model, "fraud_model.pkl")

print("Model saved successfully")

import joblib
from sklearn.ensemble import RandomForestClassifier
X = [[100, 5000, 4900],
     [200, 3000, 1000],
     [50, 2000, 1950]]
y = [0, 1, 0]  # 0 = Not Fraud, 1 = Fraud
model = RandomForestClassifier()
model.fit(X, y)
joblib.dump(model, "model.pkl")

print("Model saved successfully!")