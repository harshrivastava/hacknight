import sqlite3

# Test SQLite connection
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Create a simple test table
cursor.execute('''
CREATE TABLE IF NOT EXISTS test (
    id INTEGER PRIMARY KEY,
    name TEXT
)''')

# Insert a test row
cursor.execute("INSERT INTO test (name) VALUES (?)", ("Test successful!",))

# Read it back
cursor.execute("SELECT name FROM test")
result = cursor.fetchone()
print(f"Result from database: {result[0]}")

conn.commit()
conn.close()