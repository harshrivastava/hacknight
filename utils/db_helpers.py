"""
Database helper functions for Naborly app
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional

def get_db():
    """Get a database connection with row factory for dict-like rows"""
    conn = sqlite3.connect('naborly.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_posts(limit: int = 10, offset: int = 0) -> List[Dict]:
    """Get posts with author info, comments count, and reactions"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get posts with author info and comments count
    cursor.execute("""
        SELECT 
            p.*,
            u.username,
            u.name as author_name,
            u.avatar as author_avatar,
            (SELECT COUNT(*) FROM comments c WHERE c.post_id = p.id) as comments_count
        FROM posts p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
        LIMIT ? OFFSET ?
    """, (limit, offset))
    
    posts = [dict(row) for row in cursor.fetchall()]
    
    # Add reactions for each post
    for post in posts:
        cursor.execute("""
            SELECT emoji, COUNT(*) as count
            FROM reactions
            WHERE post_id = ?
            GROUP BY emoji
        """, (post['id'],))
        post['reactions'] = {row['emoji']: row['count'] for row in cursor.fetchall()}
    
    conn.close()
    return posts

def get_comments(post_id: int, limit: int = 5) -> List[Dict]:
    """Get comments for a post with author info"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            c.*,
            u.username,
            u.name as author_name,
            u.avatar as author_avatar
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.post_id = ?
        ORDER BY c.created_at DESC
        LIMIT ?
    """, (post_id, limit))
    
    comments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return comments

def create_post(user_id: str, message: str, media_type: Optional[str] = None, 
                media_url: Optional[str] = None) -> int:
    """Create a new post and return its ID"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO posts (user_id, message, media_type, media_url)
        VALUES (?, ?, ?, ?)
    """, (user_id, message, media_type, media_url))
    
    post_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return post_id

def add_comment(post_id: int, user_id: str, text: str) -> int:
    """Add a comment to a post and return its ID"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO comments (post_id, user_id, text)
        VALUES (?, ?, ?)
    """, (post_id, user_id, text))
    
    comment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return comment_id

def toggle_reaction(post_id: int, user_id: str, emoji: str) -> bool:
    """Toggle a reaction on a post. Returns True if added, False if removed."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if reaction exists
    cursor.execute("""
        SELECT 1 FROM reactions 
        WHERE post_id = ? AND user_id = ? AND emoji = ?
    """, (post_id, user_id, emoji))
    
    exists = cursor.fetchone() is not None
    
    if exists:
        # Remove reaction
        cursor.execute("""
            DELETE FROM reactions 
            WHERE post_id = ? AND user_id = ? AND emoji = ?
        """, (post_id, user_id, emoji))
        added = False
    else:
        # Add reaction
        cursor.execute("""
            INSERT INTO reactions (post_id, user_id, emoji)
            VALUES (?, ?, ?)
        """, (post_id, user_id, emoji))
        added = True
    
    conn.commit()
    conn.close()
    return added