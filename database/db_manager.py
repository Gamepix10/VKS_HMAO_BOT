import sqlite3

DATABASE_FILE = "data.db"

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            email TEXT,
            token TEXT
        )
    """)
    conn.commit()
    conn.close()

async def get_user(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT email, token FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return {"email": result[0], "token": result[1]} if result else None

async def save_user(user_data):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, email, token) VALUES (?, ?, ?)
    """, (user_data["user_id"], user_data["email"], user_data["token"]))
    conn.commit()
    conn.close()
