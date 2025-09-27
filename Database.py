import sqlite3

DB_NAME = "userData.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        User TEXT NOT NULL UNIQUE,
        Email TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def add_user(username, email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (User, Email, Password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False  # usuário ou email já existem
    conn.close()
    return success

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE User=? AND Password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None
