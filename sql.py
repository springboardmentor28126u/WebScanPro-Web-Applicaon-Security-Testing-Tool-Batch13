import sqlite3

# Create / connect database
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# Reset sample data
cursor.execute("DELETE FROM users")
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
conn.commit()

print("=== Vulnerable Login System ===")

username = input("Enter Username: ")
password = input("Enter Password: ")

# ❌ Vulnerable Query (String Concatenation)
query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"

print("\nExecuting Query:", query)

cursor.execute(query)
result = cursor.fetchone()

if result:
    print("Login Successful!")
else:
    print("Login Failed!")

conn.close()