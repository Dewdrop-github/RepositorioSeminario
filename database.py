import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=5432
    )

def save_message(task_id, message, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (task_id, message, status) VALUES (%s, %s, %s)",
        (task_id, message, status)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_total_messages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM messages")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count
