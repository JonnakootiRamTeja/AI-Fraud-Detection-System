import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
import shap
import smtplib
import os
from email.mime.text import MIMEText
def get_transaction():
    return {
        "amount": random.randint(100, 20000),
        "time": random.randint(1, 100000)
    }

st.set_page_config(page_title="Bank Fraud System", layout="wide")
def send_otp_email(receiver_email, otp):
    sender_email = "ramtejajonnakooti123@gmail.com"
    sender_password ="kqihoygdommhunlf"


    msg = MIMEText(f"Your OTP is: {otp}")
    msg['Subject'] = "Bank Login OTP"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
def login():
    st.title("Bank Login")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Send OTP"):
        if not email:
            st.error("Enter email first")
        elif username == "ramteja" and password == "1918":
            otp = random.randint(1000, 9999)
            st.session_state["otp"] = otp
            send_otp_email(email, otp)
            st.success("OTP sent to your email")
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
scaler = joblib.load("scaler.pkl")
explainer = shap.TreeExplainer(model)

st.markdown("""
<style>
.block-container {
    max-width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown("AI Banking Fraud Detection System")

col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", "284,807")
col2.metric("Fraud Cases", "492")
col3.metric("Fraud Rate", "0.17%")

if "history" not in st.session_state:
    st.session_state["history"] = []

st.subheader("Enter Transaction")
pay = st.button("Pay Now")
check = st.button("Check Fraud")

amount = st.number_input("Transaction Amount", min_value=0.0)
time_val = st.number_input("Transaction Time", min_value=0.0)
if pay:
    st.success("Payment Processing...")

if st.button("Generate Live Transaction"):
    txn = get_transaction()
    amount = txn["amount"]
    time_val = txn["time"]
    st.info(f"Auto Generated → ₹{amount}, Time: {time_val}")

if check:
    columns = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']

    data_dict = {col: np.random.uniform(-2, 2) for col in columns}
    data_dict['Time'] = time_val
    data_dict['Amount'] = amount

    data_df = pd.DataFrame([data_dict])
    data_scaled = scaler.transform(data_df)

    prediction = model.predict(data_scaled)
    probability = model.predict_proba(data_scaled)

    shap_values = explainer.shap_values(data_scaled)

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

        st.subheader("Fraud Explanation")
feature_names = ['Time'] + [f'V{i}' for i in range(1,29)] + ['Amount']

try:
    if isinstance(shap_values, list):
        if len(shap_values) > 1:
            values = shap_values[1][0]
        else:
            values = shap_values[0]
    else:
        values = shap_values[0]

    values = np.array(values).flatten()

except Exception as e:
    values = np.zeros(len(feature_names))

if len(values) != len(feature_names):
    values = np.resize(values, len(feature_names))

shap_df = pd.DataFrame({
    "Feature": feature_names,
    "Impact": values
})
shap_df = shap_df.sort_values(by="Impact", key=abs, ascending=False)
st.write("Top Reasons:")
st.dataframe(shap_df.head(5))

st.subheader("Live Transactions")

if st.button("Start Live Simulation"):
    columns = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']

    for i in range(5):
        amt = random.randint(100, 10000)
        t = random.randint(1, 100000)

        data_dict = {col: np.random.uniform(-2, 2) for col in columns}
        data_dict['Time'] = t
        data_dict['Amount'] = amt

        data_df = pd.DataFrame([data_dict])
        data_scaled = scaler.transform(data_df)

        pred = model.predict(data_scaled)
        prob = model.predict_proba(data_scaled)

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
        label="Download Report",
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