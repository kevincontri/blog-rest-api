import sqlite3

def db_connect():
    conn = sqlite3.connect("blog.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def _ensure_users_schema(cursor):
    columns = {
        row[1]
        for row in cursor.execute("PRAGMA table_info(users)").fetchall()
    }
    if "password_hash" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
    if "created_at" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN created_at TEXT")

def init_db():
    conn = db_connect()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT,
            password_hash TEXT,
            created_at TEXT
        )""")
    _ensure_users_schema(c)

    c.execute("""CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            author_id TEXT,
            created_at TEXT,
            FOREIGN KEY(author_id) REFERENCES users(id)
        )""")

    c.execute("""CREATE TABLE IF NOT EXISTS comments (
            id TEXT PRIMARY KEY,
            content TEXT,
            post_id TEXT,
            author_id TEXT,
            created_at TEXT,
            FOREIGN KEY(post_id) REFERENCES posts(id),
            FOREIGN KEY(author_id) REFERENCES users(id)
    )""")

    conn.commit()

    conn.close()
