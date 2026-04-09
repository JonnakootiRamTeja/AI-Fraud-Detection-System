import joblib
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

model = joblib.load("fraud_model.pkl")
scaler = joblib.load("scaler.pkl")
columns = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']

t = 50000       
amt = 8000     

data_dict = {col: 0 for col in columns}
data_dict['Time'] = t
data_dict['Amount'] = amt

data_df = pd.DataFrame([data_dict])

data_scaled = scaler.transform(data_df)

prediction = model.predict(data_scaled)
probability = model.predict_proba(data_scaled)

if prediction[0] == 0:
    print(f"Transaction is NORMAL (Prob: {probability[0][1]:.2f})")
else:
    print(f"Fraudulent Transaction Detected (Prob: {probability[0][1]:.2f})")