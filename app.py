import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import random

st.set_page_config(page_title="Bank Fraud System", layout="wide")
def login():
    st.title("Bank Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Send OTP"):
        if username == "ramteja" and password == "1918":
            otp = random.randint(1000, 9999)
            st.session_state["otp"] = otp
            st.success(f"OTP Sent: {otp}")
        else:
            st.error("Invalid Username or Password")

    otp_input = st.text_input("Enter OTP")

    if st.button("Login"):
        if otp_input and int(otp_input) == st.session_state.get("otp", 0):
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid OTP")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()
model = joblib.load("fraud_model.pkl")

st.title("AI Banking Fraud Detection Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", "284,807")
col2.metric("Fraud Cases", "492")
col3.metric("Fraud Rate", "0.17%")

if "history" not in st.session_state:
    st.session_state["history"] = []

st.subheader("Enter Transaction")

amount = st.number_input("Transaction Amount", min_value=0.0)
time_val = st.number_input("Transaction Time", min_value=0.0)

features = np.zeros(30)
features[0] = amount
features[1] = time_val
features = features.reshape(1, -1)

if st.button("Check Transaction"):
    prediction = model.predict(features)
    probability = model.predict_proba(features)

    result = "Fraud" if prediction[0] == 1 else "Safe"

    if result == "Fraud":
        st.error(f"Fraud Detected (Prob: {probability[0][1]:.2f})")
    else:
        st.success(f"Safe Transaction (Prob: {probability[0][1]:.2f})")

    st.session_state["history"].append({
        "Amount": amount,
        "Time": time_val,
        "Result": result,
        "Probability": round(probability[0][1], 2)
    })

st.subheader("Live Transactions")
if st.button("Start Live Simulation"):
    for i in range(5):
        amt = random.randint(100, 10000)
        t = random.randint(1, 100000)
        data = np.zeros((1, 30))
        data[0][0] = amt
        data[0][1] = t
        pred = model.predict(data)
        prob = model.predict_proba(data)
        result = "FRAUD" if pred[0] == 1 else "SAFE"
        if result == "FRAUD":
            st.error(f"₹{amt} → FRAUD ({prob[0][1]:.2f})")
        else:
            st.success(f"₹{amt} → SAFE ({prob[0][1]:.2f})")
        time.sleep(1)

st.subheader("Transaction History")

if st.session_state["history"]:
    df = pd.DataFrame(st.session_state["history"])
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Report",
        data=csv,
        file_name="fraud_report.csv",
        mime="text/csv"
    )

st.subheader("Fraud vs Safe")
if st.session_state["history"]:
    df = pd.DataFrame(st.session_state["history"])
    counts = df["Result"].value_counts()
    fig, ax = plt.subplots()
    counts.plot(kind='bar', ax=ax)
    st.pyplot(fig)