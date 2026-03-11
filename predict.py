import joblib
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

model = joblib.load("fraud_model.pkl")
columns = [f"V{i}" for i in range(1,29)] + ["Time","Amount"]

sample = pd.DataFrame(np.random.rand(1,30), columns=columns)

prediction = model.predict(sample)

if prediction[0] == 0:
    print("Transaction is NORMAL")
else:
    print("Fraudulent Transaction Detected")