import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bank Fraud System", layout="wide")
def login():
    st.title("Bank Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid Username or Password")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

model = joblib.load("fraud_model.pkl")
st.title(" AI Banking Fraud Detection Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", "284,807")
col2.metric("Fraud Cases", "492")
col3.metric("Fraud Rate", "0.17%")
st.subheader("Check Transaction")

features = []
for i in range(30):
    value = st.number_input(f"Feature {i}", value=0.0)
    features.append(value)
features = np.array(features).reshape(1, -1)
if st.button("Check Transaction"):
    prediction = model.predict(features)
    probability = model.predict_proba(features)
    if prediction[0] == 1:
        st.error(f" Fraud Detected (Probability: {probability[0][1]:.2f})")
    else:
        st.success(f"Safe Transaction (Probability: {probability[0][1]:.2f})")
st.subheader("Live Transactions")

if st.button("Generate Live Transactions"):
    data = np.random.rand(5, 30)
    df = pd.DataFrame(data, columns=[f"Feature {i}" for i in range(30)])
    st.write(df)
    preds = model.predict(data)
    for i, p in enumerate(preds):
        if p == 1:
            st.error(f"Transaction {i+1}: FRAUD")
        else:
            st.success(f"Transaction {i+1}: SAFE")
st.subheader("Fraud Distribution")

data = pd.read_csv("creditcard.csv")

fig, ax = plt.subplots()
sns.countplot(x="Class", data=data)
st.pyplot(fig)
st.subheader("Model Performance")

from sklearn.metrics import confusion_matrix

y_true = [0,1,0,1,0]
y_pred = [0,1,0,0,0]

cm = confusion_matrix(y_true, y_pred)

fig2, ax2 = plt.subplots()
sns.heatmap(cm, annot=True, fmt='d', ax=ax2)
st.pyplot(fig2)