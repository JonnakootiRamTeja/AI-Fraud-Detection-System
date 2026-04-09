import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, roc_auc_score
import joblib

df = pd.read_csv("creditcard.csv")
fraud = df[df["Class"] == 1]
normal = df[df["Class"] == 0]

fraud_upsampled = resample(fraud,replace=True,n_samples=len(normal),random_state=42)
df_balanced = pd.concat([normal, fraud_upsampled])

X = df_balanced.drop("Class", axis=1)
y = df_balanced["Class"]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
model = RandomForestClassifier()
model.fit(X_train, y_train)
joblib.dump(model, "fraud_model.pkl")
joblib.dump(scaler, "scaler.pkl")
print("Balanced model trained!")
y_probs = model.predict_proba(X_test)[:, 1]
threshold = 0.3
y_pred = (y_probs > threshold).astype(int)
print("ROC-AUC Score:", roc_auc_score(y_test, y_probs))
print(classification_report(y_test, y_pred))