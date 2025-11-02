"""
Setup script for Naborly database
This creates all necessary tables and adds some sample data
"""
import sqlite3
import json
from datetime import datetime

def setup_database():
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('naborly.db')
    cursor = conn.cursor()
    
    print("Creating tables...")
    
    # Create all tables
    cursor.executescript('''
    -- Users table
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        avatar TEXT DEFAULT '👤',
        bio TEXT,
        followers INTEGER DEFAULT 0,
        following INTEGER DEFAULT 0,
        password_hash TEXT
    );

    -- Posts table
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        message TEXT,
        media_type TEXT,
        media_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    -- Comments table
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id TEXT NOT NULL,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(post_id) REFERENCES posts(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    -- Reactions table
    CREATE TABLE IF NOT EXISTS reactions (
        post_id INTEGER NOT NULL,
        user_id TEXT NOT NULL,
        emoji TEXT NOT NULL,
        FOREIGN KEY(post_id) REFERENCES posts(id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        PRIMARY KEY(post_id, user_id, emoji)
    );
    ''')
    
    print("Adding sample data...")
    
    # Add sample users
    sample_users = [
        ('u1', 'neha.singh', 'Neha Singh', '👩', 'Living life one photo at a time 📸', 1234, 891),
        ('u2', 'amit.kumar', 'Amit Kumar', '👨', 'Travel | Photography | Coffee', 2345, 1023),
        ('u3', 'saira.khan', 'Saira Khan', '👩', 'Digital Artist 🎨', 3456, 892)
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO users (id, username, name, avatar, bio, followers, following)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_users)
    
    # Add sample posts
    sample_posts = [
        ('u1', 'Just had an amazing discussion about sustainable community development! 🌱 Great to see so many neighbors interested in making our area greener.'),
        ('u2', 'Beautiful sunrise view from our community park! Starting the day with positivity. 🌅'),
        ('u3', 'Check out this amazing talent from our community art festival! The creativity of our young artists is incredible. 🎨')
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO posts (user_id, message)
    VALUES (?, ?)
    ''', sample_posts)
    
    # Get the first post's ID
    cursor.execute("SELECT id FROM posts ORDER BY id ASC LIMIT 1")
    first_post_id = cursor.fetchone()[0]
    
    # Add a sample comment
    cursor.execute('''
    INSERT OR IGNORE INTO comments (post_id, user_id, text)
    VALUES (?, ?, ?)
    ''', (first_post_id, 'u2', 'Count me in for the cleanup drives! When do we start?'))
    
    # Add some sample reactions
    sample_reactions = [
        (first_post_id, 'u2', '❤️'),
        (first_post_id, 'u3', '👏')
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO reactions (post_id, user_id, emoji)
    VALUES (?, ?, ?)
    ''', sample_reactions)
    
    # Commit changes and close
    conn.commit()
    conn.close()
    
    print("Database setup complete! Created naborly.db with sample data.")
    print("\nTables created:")
    print("- users (for user profiles)")
    print("- posts (for community posts)")
    print("- comments (for post comments)")
    print("- reactions (for post reactions)")

if __name__ == "__main__":
    setup_database()