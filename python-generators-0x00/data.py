import sqlite3

# Create a database connection
conn = sqlite3.connect("alx-prodev")

# Close the connection
conn.close()


# Connect to the database
conn = sqlite3.connect("alx-prodev.db")

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

# Insert sample data
cursor.executemany("""
INSERT INTO users (name, age) VALUES (?, ?)
""", [
    ('Alice', 30),
    ('Bob', 50),
    ('Charlie', 42),
    ('Diana', 25)
])

# Commit the changes and close the connection
conn.commit()
conn.close()


# Connect to the database
conn = sqlite3.connect("example.db")
# Fetch data
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")

for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()
