import os
import sqlite3

def load_documents():
    documents = [
        {'title': 'Конституция', 'file_path': 'documents/constitutionrf.pdf'},
        # Add other documents
    ]

    conn = sqlite3.connect('law_bot.db')
    cursor = conn.cursor()

    for doc in documents:
        with open(doc['file_path'], 'rb') as file:
            pdf_data = file.read()
            cursor.execute('INSERT INTO documents (title, content) VALUES (?, ?)', (doc['title'], pdf_data))

    conn.commit()
    conn.close()

load_documents()
