import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

model = joblib.load("fraud_model.pkl")

st.title("AI-Powered Fraud Detection Dashboard")

st.write("Real-Time Transaction Monitoring")

features = []

for i in range(30):
    value = st.number_input(f"Feature {i}")
    features.append(value)

features = np.array(features).reshape(1,-1)

if st.button("Check Transaction"):

    prediction = model.predict(features)
    probability = model.predict_proba(features)

    st.subheader("Prediction Result")

    if prediction[0] == 1:
        st.error("⚠ Fraudulent Transaction Detected")
    else:
        st.success("✔ Legitimate Transaction")
    st.write("Fraud Probability:", probability[0][1])

st.subheader("Transaction Visualization")
data = pd.read_csv("creditcard.csv")
fig, ax = plt.subplots()
sns.countplot(x="Class", data=data)
st.pyplot(fig)