import streamlit as st
import sqlite3
import random

# ---------------- PAGE ----------------
st.set_page_config(page_title="Wallet App", layout="centered")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT,
    balance INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    receiver TEXT,
    amount INTEGER,
    status TEXT
)
""")

conn.commit()

# ---------------- FUNCTIONS ----------------

def register_user(email, password):
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (email, password, 5000))
        conn.commit()
        return True
    except:
        return False

def login_user(email, password):
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    return c.fetchone()

def get_balance(email):
    c.execute("SELECT balance FROM users WHERE email=?", (email,))
    result = c.fetchone()
    return result[0] if result else 0

def update_balance(email, amount):
    c.execute("UPDATE users SET balance=? WHERE email=?", (amount, email))
    conn.commit()

def save_transaction(sender, receiver, amount, status):
    c.execute(
        "INSERT INTO transactions (sender, receiver, amount, status) VALUES (?, ?, ?, ?)",
        (sender, receiver, amount, status)
    )
    conn.commit()

# ---------------- OTP ----------------
def send_otp(email):
    otp = random.randint(1000, 9999)
    st.session_state["otp"] = otp
    st.session_state["otp_email"] = email
    st.success(f"OTP (Demo): {otp}")  # replace with email later

# ---------------- MENU ----------------
menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

# ---------------- SIGNUP ----------------
if menu == "Signup":
    st.title("Signup")

    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_pass")

    if st.button("Signup", key="signup_btn"):
        if register_user(email, password):
            st.success("Account Created ✅")
        else:
            st.warning("User already exists ❌")

# ---------------- LOGIN ----------------
if menu == "Login":
    st.title("Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    col1, col2 = st.columns(2)

    # SEND OTP
    with col1:
        if st.button("Send OTP", key="send_otp_btn"):
            if login_user(email, password):
                send_otp(email)
            else:
                st.error("Invalid credentials ❌")

    # VERIFY OTP
    with col2:
        user_otp = st.text_input("Enter OTP", key="otp_input")

        if st.button("Verify OTP", key="verify_btn"):
            if str(user_otp) == str(st.session_state.get("otp")):
                st.session_state["logged_in"] = True
                st.session_state["user"] = email
                st.success("Login Successful ✅")
            else:
                st.error("Wrong OTP ❌")

# ---------------- DASHBOARD ----------------
if st.session_state.get("logged_in"):

    email = st.session_state.get("user")
    balance = get_balance(email)

    st.title("💳 Dashboard")
    st.write(f"Welcome: {email}")
    st.write(f"Balance: ₹{balance}")

    receiver = st.text_input("Receiver Email", key="receiver")
    amount = st.number_input("Amount", min_value=1, key="amount")

    if st.button("Send Money", key="send_money_btn"):
        receiver_balance = get_balance(receiver)

        if amount > 5000:
            st.warning("⚠️ Fraud detected!")
            save_transaction(email, receiver, amount, "Fraud")

        else:
            if balance >= amount:
                update_balance(email, balance - amount)
                update_balance(receiver, receiver_balance + amount)
                save_transaction(email, receiver, amount, "Success")
                st.success("Money Sent ✅")
            else:
                st.error("Insufficient balance ❌")

    # HISTORY
    st.subheader("Transactions")

    c.execute(
        "SELECT sender, receiver, amount, status FROM transactions WHERE sender=? OR receiver=?",
        (email, email)
    )
    data = c.fetchall()

    for row in data:
        st.write(f"{row[0]} → {row[1]} | ₹{row[2]} | {row[3]}")

    if st.button("Logout", key="logout_btn"):
        st.session_state.clear()