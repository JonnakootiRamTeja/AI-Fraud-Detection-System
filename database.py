import sqlite3

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

def add_user(email, password):
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (email, password, 1000))
    conn.commit()

def login_user(email, password):
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    return c.fetchone()

def get_balance(email):
    c.execute("SELECT balance FROM users WHERE email=?", (email,))
    return c.fetchone()[0]