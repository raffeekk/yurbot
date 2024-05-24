import sqlite3

def init_db():
    conn = sqlite3.connect('law_bot.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS documents (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        content BLOB)''')  # Change content to BLOB to store PDF files
    cursor.execute('''CREATE TABLE IF NOT EXISTS templates (
                        id INTEGER PRIMARY KEY,
                        title TEXT,
                        content TEXT)''')
    conn.commit()
    conn.close()

#init_db()
