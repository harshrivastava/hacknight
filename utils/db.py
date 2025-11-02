"""
Simple SQLite helpers for Naborly (beginner-friendly).

Provides:
- init_db(path=None) to create the database file and all required tables
- context manager connect_db(path=None) to get a connection (commits on success)
- high-level CRUD helpers: create_user, get_user_by_username, create_post, get_posts,
  add_comment, toggle_reaction, get_notifications, upsert_ration_rate, etc.

Usage (in Streamlit):
    from utils import db
    db.init_db()  # create file and tables if missing
    posts = db.get_posts(limit=10, offset=0)

Notes:
- For simplicity this module opens a new connection for each operation via the
  context manager. In Streamlit you can cache a single connection with
  `st.cache_resource(lambda: sqlite3.connect(db_path, check_same_thread=False))` if
  you prefer a persistent connection.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, List, Dict, Any
import json


DEFAULT_DB = Path(__file__).parent.parent / "naborly.db"


def get_db_path(path: Optional[str] = None) -> Path:
    if path:
        return Path(path)
    return DEFAULT_DB


@contextmanager
def connect_db(path: Optional[str] = None):
    """Context manager yielding a sqlite3.Connection.

    Commits on successful exit, rolls back on exception.
    Uses row factory to return dict-like rows (sqlite3.Row).
    """
    db_path = get_db_path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path), detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(path: Optional[str] = None) -> None:
    """Create database file and all tables if they don't exist."""
    schema = _create_schema_sql()
    with connect_db(path) as conn:
        cur = conn.cursor()
        cur.executescript(schema)
        # Recommended pragmas for better concurrency on local apps
        cur.execute("PRAGMA journal_mode=WAL;")


def _create_schema_sql() -> str:
    """Return a SQL script that creates all necessary tables."""
    return """
    -- users: basic profile + hashed password
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        avatar TEXT,
        bio TEXT,
        followers INTEGER DEFAULT 0,
        following INTEGER DEFAULT 0,
        password_hash TEXT
    );

    -- posts: authored by a user
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        message TEXT,
        media_type TEXT,
        media_blob BLOB,
        media_mime TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    -- comments on posts
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id TEXT NOT NULL,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(post_id) REFERENCES posts(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    -- reactions: a user can react with the same emoji only once per post
    CREATE TABLE IF NOT EXISTS reactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id TEXT NOT NULL,
        emoji TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(post_id) REFERENCES posts(id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        UNIQUE(post_id, user_id, emoji)
    );

    -- notifications for users (simple queue)
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        payload TEXT NOT NULL, -- JSON blob with notification data
        read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );

    -- government ration rates data
    CREATE TABLE IF NOT EXISTS ration_rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT,
        district TEXT,
        month_year TEXT, -- e.g. '2025-11'
        commodity TEXT,
        rate REAL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- complaints submitted by residents
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        description TEXT,
        contact TEXT,
        location TEXT,
        status TEXT DEFAULT 'submitted',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- service providers directory (electrician, plumber, tuition, etc.)
    CREATE TABLE IF NOT EXISTS service_providers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        name TEXT,
        contact TEXT,
        area TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- vendors (vegetables, fruits, essentials)
    CREATE TABLE IF NOT EXISTS vendors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        name TEXT,
        contact TEXT,
        area TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- government / administrative bodies directory
    CREATE TABLE IF NOT EXISTS government_bodies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        contact TEXT,
        hours TEXT,
        location TEXT,
        website TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """


# ----------------------
# High-level helpers
# ----------------------

def create_user(user_id: str, username: str, name: str, password_hash: Optional[str] = None,
                avatar: str = "👤", bio: str = "") -> Dict[str, Any]:
    """Insert a new user. Returns the created user row as dict."""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users(id, username, name, avatar, bio, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, username, name, avatar, bio, password_hash)
        )
        # Fetch and return
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        return dict(row) if row else {}


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        return dict(row) if row else None


def create_post(user_id: str, message: str = None, media_type: str = None,
                media_blob: bytes = None, media_mime: str = None) -> int:
    """Create a post. Returns new post id."""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO posts(user_id, message, media_type, media_blob, media_mime) VALUES (?, ?, ?, ?, ?)",
            (user_id, message, media_type, media_blob, media_mime)
        )
        return cur.lastrowid


def add_comment(post_id: int, user_id: str, text: str) -> int:
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO comments(post_id, user_id, text) VALUES (?, ?, ?)",
            (post_id, user_id, text)
        )
        return cur.lastrowid


def toggle_reaction(post_id: int, user_id: str, emoji: str) -> bool:
    """Toggle a reaction: returns True if added, False if removed."""
    with connect_db() as conn:
        cur = conn.cursor()
        # Check if exists
        cur.execute("SELECT id FROM reactions WHERE post_id = ? AND user_id = ? AND emoji = ?",
                    (post_id, user_id, emoji))
        row = cur.fetchone()
        if row:
            cur.execute("DELETE FROM reactions WHERE id = ?", (row[0],))
            return False
        else:
            cur.execute("INSERT INTO reactions(post_id, user_id, emoji) VALUES (?, ?, ?)",
                        (post_id, user_id, emoji))
            return True


def get_posts(limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
    """Return posts joined with author info and aggregated counts.

    Each row will include: post fields, author (username, name, avatar), comment_count and reaction_summary (JSON)
    """
    with connect_db() as conn:
        cur = conn.cursor()
        # Core posts + author
        cur.execute(
            """
            SELECT p.*, u.username, u.name as author_name, u.avatar as author_avatar,
                   (
                       SELECT COUNT(*) FROM comments c WHERE c.post_id = p.id
                   ) AS comment_count
            FROM posts p
            JOIN users u ON u.id = p.user_id
            ORDER BY p.created_at DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset)
        )
        posts = [dict(r) for r in cur.fetchall()]

        # For each post get reaction summary
        for post in posts:
            cur.execute("SELECT emoji, COUNT(*) as cnt FROM reactions WHERE post_id = ? GROUP BY emoji", (post["id"],))
            reactions = {r["emoji"]: r["cnt"] for r in cur.fetchall()}
            post["reaction_summary"] = reactions

        return posts


def get_comments_for_post(post_id: int, limit: int = 10) -> List[Dict[str, Any]]:
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT c.*, u.username, u.name as author_name, u.avatar as author_avatar FROM comments c JOIN users u ON u.id = c.user_id WHERE c.post_id = ? ORDER BY c.created_at ASC LIMIT ?",
            (post_id, limit)
        )
        return [dict(r) for r in cur.fetchall()]


def add_notification(user_id: str, payload: Dict[str, Any]) -> int:
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO notifications(user_id, payload) VALUES (?, ?)", (user_id, json.dumps(payload)))
        return cur.lastrowid


def get_notifications(user_id: str, only_unread: bool = True) -> List[Dict[str, Any]]:
    with connect_db() as conn:
        cur = conn.cursor()
        if only_unread:
            cur.execute("SELECT * FROM notifications WHERE user_id = ? AND read = 0 ORDER BY created_at DESC", (user_id,))
        else:
            cur.execute("SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        rows = [dict(r) for r in cur.fetchall()]
        for r in rows:
            try:
                r["payload"] = json.loads(r["payload"])
            except Exception:
                pass
        return rows


def upsert_ration_rate(state: str, district: str, month_year: str, commodity: str, rate: float) -> int:
    """Insert a new ration rate entry. This keeps historic rows; callers can query latest per month_year."""
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO ration_rates(state, district, month_year, commodity, rate) VALUES (?, ?, ?, ?, ?)",
            (state, district, month_year, commodity, rate)
        )
        return cur.lastrowid


def query_ration_rates(state: Optional[str] = None, district: Optional[str] = None, month_year: Optional[str] = None) -> List[Dict[str, Any]]:
    with connect_db() as conn:
        cur = conn.cursor()
        q = "SELECT * FROM ration_rates WHERE 1=1"
        params: List[Any] = []
        if state:
            q += " AND state = ?"
            params.append(state)
        if district:
            q += " AND district = ?"
            params.append(district)
        if month_year:
            q += " AND month_year = ?"
            params.append(month_year)
        q += " ORDER BY updated_at DESC"
        cur.execute(q, params)
        return [dict(r) for r in cur.fetchall()]


# ----------------------
# Complaints & directory helpers
# ----------------------

def create_complaint(category: str, description: str, contact: str = None, location: str = None) -> int:
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO complaints (category, description, contact, location) VALUES (?, ?, ?, ?)",
            (category, description, contact, location)
        )
        return cur.lastrowid


def get_complaints(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM complaints ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )
        return [dict(r) for r in cur.fetchall()]


def create_service_provider(category: str, name: str, contact: str, area: str = None, description: str = None) -> int:
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO service_providers (category, name, contact, area, description) VALUES (?, ?, ?, ?, ?)",
            (category, name, contact, area, description)
        )
        return cur.lastrowid


def get_service_providers(category: Optional[str] = None, q: Optional[str] = None, limit: int = 200) -> List[Dict[str, Any]]:
    with connect_db() as conn:
        cur = conn.cursor()
        if category:
            cur.execute("SELECT * FROM service_providers WHERE category = ? ORDER BY created_at DESC LIMIT ?", (category, limit))
        elif q:
            like = f"%{q}%"
            cur.execute("SELECT * FROM service_providers WHERE name LIKE ? OR area LIKE ? OR description LIKE ? ORDER BY created_at DESC LIMIT ?", (like, like, like, limit))
        else:
            cur.execute("SELECT * FROM service_providers ORDER BY created_at DESC LIMIT ?", (limit,))
        return [dict(r) for r in cur.fetchall()]


def create_vendor(vtype: str, name: str, contact: str, area: str = None, notes: str = None) -> int:
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO vendors (type, name, contact, area, notes) VALUES (?, ?, ?, ?, ?)",
            (vtype, name, contact, area, notes)
        )
        return cur.lastrowid


def get_vendors(vtype: Optional[str] = None, q: Optional[str] = None, limit: int = 200) -> List[Dict[str, Any]]:
    with connect_db() as conn:
        cur = conn.cursor()
        if vtype:
            cur.execute("SELECT * FROM vendors WHERE type = ? ORDER BY created_at DESC LIMIT ?", (vtype, limit))
        elif q:
            like = f"%{q}%"
            cur.execute("SELECT * FROM vendors WHERE name LIKE ? OR area LIKE ? OR notes LIKE ? ORDER BY created_at DESC LIMIT ?", (like, like, like, limit))
        else:
            cur.execute("SELECT * FROM vendors ORDER BY created_at DESC LIMIT ?", (limit,))
        return [dict(r) for r in cur.fetchall()]


def add_government_body(name: str, department: str, contact: str, hours: str = None, location: str = None, website: str = None) -> int:
    with connect_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO government_bodies (name, department, contact, hours, location, website) VALUES (?, ?, ?, ?, ?, ?)",
            (name, department, contact, hours, location, website)
        )
        return cur.lastrowid


def get_government_bodies(department: Optional[str] = None, q: Optional[str] = None, limit: int = 200) -> List[Dict[str, Any]]:
    with connect_db() as conn:
        cur = conn.cursor()
        if department:
            cur.execute("SELECT * FROM government_bodies WHERE department = ? ORDER BY created_at DESC LIMIT ?", (department, limit))
        elif q:
            like = f"%{q}%"
            cur.execute("SELECT * FROM government_bodies WHERE name LIKE ? OR location LIKE ? ORDER BY created_at DESC LIMIT ?", (like, like, limit))
        else:
            cur.execute("SELECT * FROM government_bodies ORDER BY created_at DESC LIMIT ?", (limit,))
        return [dict(r) for r in cur.fetchall()]


def import_complaints_from_json(path: Optional[str] = None) -> int:
    """Import complaints from a JSON file into the complaints table. Returns number imported."""
    json_path = Path(path) if path else (Path(__file__).parent.parent / "complaints.json")
    if not json_path.exists():
        return 0
    try:
        data = json.loads(json_path.read_text())
        count = 0
        for item in data:
            create_complaint(item.get('category','Other'), item.get('description',''), item.get('contact'), item.get('location'))
            count += 1
        return count
    except Exception:
        return 0


def import_services_from_json(path: Optional[str] = None) -> int:
    """Import providers/vendors from a services JSON into the DB. Returns total imported."""
    json_path = Path(path) if path else (Path(__file__).parent.parent / "services_listings.json")
    if not json_path.exists():
        return 0
    try:
        data = json.loads(json_path.read_text())
        providers = data.get('providers', []) if isinstance(data, dict) else []
        vendors = data.get('vendors', []) if isinstance(data, dict) else []
        count = 0
        for p in providers:
            create_service_provider(p.get('category','General'), p.get('name',''), p.get('contact',''), p.get('area'), p.get('description'))
            count += 1
        for v in vendors:
            create_vendor(v.get('type','General'), v.get('name',''), v.get('contact',''), v.get('area'), v.get('notes'))
            count += 1
        return count
    except Exception:
        return 0
