import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('users.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

sample_users = [
        ("John Doe", "john@example.com", "password123"),
        ("Jane Smith", "jane@example.com", "secret456"),
        ("Bob Johnson", "bob@example.com", "qwerty789")
    ]


# Insert sample users
for name, email, password in sample_users:
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"User {email} already exists")
    except sqlite3.Error as e:
        print(f"Error inserting user {email}: {e}")

conn.commit()
conn.close()

print("Database initialized with sample data")