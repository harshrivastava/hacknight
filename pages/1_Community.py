"""
InstaCommunity - An Instagram-style Community Feed
A Streamlit-powered social feed with posts, reactions, comments, and media sharing.
"""

import streamlit as st
import json
import os
from datetime import datetime
from PIL import Image
import io
from pathlib import Path
import time
import random

# -----------------------------
# Constants and Data
# -----------------------------

POSTS_FILE = "community_posts.json"
POSTS_PER_PAGE = 5

SAMPLE_USERS = [
    {
        "id": "u1",
        "username": "neha.singh",
        "name": "Neha Singh",
        "avatar": "👩",
        "bio": "Living life one photo at a time 📸 | Food lover 🍕",
        "followers": 1234,
        "following": 891
    },
    {
        "id": "u2",
        "username": "amit.kumar",
        "name": "Amit Kumar",
        "avatar": "👨",
        "bio": "Travel | Photography | Coffee ✈️ ☕",
        "followers": 2345,
        "following": 1023
    },
    {
        "id": "u3",
        "username": "saira.khan",
        "name": "Saira Khan",
        "avatar": "👩",
        "bio": "Digital Artist 🎨 | Cat lover 🐱",
        "followers": 3456,
        "following": 892
    },
    {
        "id": "u4",
        "username": "guest.user",
        "name": "Guest User",
        "avatar": "👤",
        "bio": "Community Member",
        "followers": 0,
        "following": 0
    }
]

REACTIONS = {
    "❤️": "Love",
    "🔥": "Fire",
    "👏": "Clap",
    "🙌": "Praise",
    "😍": "Heart Eyes"
}

# -----------------------------
# Helper Functions
# -----------------------------

def get_default_posts():
    """Return default posts with different types of content"""
    return [
        {
            "id": "1",
            "user": "Neha Singh",
            "time": "2025-11-02 10:30",
            "message": "Just had an amazing discussion about sustainable community development! 🌱 Great to see so many neighbors interested in making our area greener. Here are some key points we discussed:\n\n• Solar panel initiatives\n• Community garden expansion\n• Weekly cleanup drives\n• Water conservation methods\n\nLet's make our community eco-friendly! 💚",
            "media": None,
            "reactions": {
                "❤️": ["Amit Kumar", "Saira Khan"],
                "👏": ["Guest User"]
            },
            "comments": [
                {
                    "user": "Amit Kumar",
                    "avatar": "👨",
                    "time": "2025-11-02 10:35",
                    "text": "Count me in for the cleanup drives! When do we start?"
                }
            ]
        },
        {
            "id": "2",
            "user": "Amit Kumar",
            "time": "2025-11-02 09:15",
            "message": "Beautiful sunrise view from our community park! Starting the day with positivity. 🌅",
            "media": {
                "type": "image",
                "data": "https://images.unsplash.com/photo-1544998796-3e777c66c2a8",
                "mime": "image/jpeg"
            },
            "reactions": {
                "❤️": ["Neha Singh", "Saira Khan"],
                "😍": ["Guest User"]
            },
            "comments": [
                {
                    "user": "Saira Khan",
                    "avatar": "👩",
                    "time": "2025-11-02 09:20",
                    "text": "This is why I love our community park! Such peaceful mornings."
                }
            ]
        },
        {
            "id": "3",
            "user": "Saira Khan",
            "time": "2025-11-02 08:00",
            "message": "Check out this amazing talent from our community's art festival! The creativity of our young artists is incredible. 🎨",
            "media": {
                "type": "video",
                "data": "https://example.com/sample-video.mp4",
                "mime": "video/mp4"
            },
            "reactions": {
                "🔥": ["Neha Singh", "Amit Kumar"],
                "👏": ["Guest User"]
            },
            "comments": []
        },
        {
            "id": "4",
            "user": "Guest User",
            "time": "2025-11-02 07:45",
            "message": "Quick reminder: Tomorrow's community meeting will be held in the main hall at 6 PM. Topics include:\n\n📌 Winter festival planning\n📌 New playground equipment\n📌 Local business initiatives\n\nDon't forget to bring your suggestions!",
            "media": None,
            "reactions": {
                "👍": ["Neha Singh"],
                "❤️": ["Amit Kumar"]
            },
            "comments": [
                {
                    "user": "Neha Singh",
                    "avatar": "👩",
                    "time": "2025-11-02 07:50",
                    "text": "Thanks for the reminder! Looking forward to discussing the winter festival."
                }
            ]
        }
    ]

def load_posts():
    """Load posts from JSON file or return default posts if file doesn't exist"""
    try:
        if os.path.exists(POSTS_FILE):
            with open(POSTS_FILE, 'r') as f:
                content = f.read()
                if not content.strip():  # If file is empty
                    default_posts = get_default_posts()
                    with open(POSTS_FILE, 'w') as f:
                        json.dump(default_posts, f, indent=2)
                    return default_posts
                return json.loads(content)
        else:
            # Create file with default posts
            default_posts = get_default_posts()
            with open(POSTS_FILE, 'w') as f:
                json.dump(default_posts, f, indent=2)
            return default_posts
    except json.JSONDecodeError as e:
        st.error(f"Error decoding posts file: {e}")
        # Backup corrupted file and create new one
        if os.path.exists(POSTS_FILE):
            backup_file = f"{POSTS_FILE}.backup"
            os.rename(POSTS_FILE, backup_file)
            st.warning(f"Corrupted posts file backed up to {backup_file}")
        with open(POSTS_FILE, 'w') as f:
            json.dump([], f)
        return []
    except Exception as e:
        st.error(f"Error loading posts: {e}")
        return []

def save_posts(posts):
    """Save posts to JSON file"""
    try:
        # Validate posts data structure
        if not isinstance(posts, list):
            raise ValueError("Posts must be a list")
            
        # Ensure each post has required fields
        for post in posts:
            if not isinstance(post, dict):
                raise ValueError("Each post must be a dictionary")
            required_fields = ["id", "user", "time"]
            missing_fields = [field for field in required_fields if field not in post]
            if missing_fields:
                raise ValueError(f"Post missing required fields: {', '.join(missing_fields)}")
        
        # Create backup of existing file
        if os.path.exists(POSTS_FILE):
            backup_file = f"{POSTS_FILE}.bak"
            try:
                with open(POSTS_FILE, 'r') as src, open(backup_file, 'w') as dst:
                    dst.write(src.read())
            except Exception as e:
                st.warning(f"Could not create backup: {e}")
        
        # Save new data
        with open(POSTS_FILE, 'w') as f:
            json.dump(posts, f, indent=2)  # Use indent for readable format
            
    except Exception as e:
        st.error(f"Error saving posts: {e}")
        if os.path.exists(f"{POSTS_FILE}.bak"):
            try:
                os.replace(f"{POSTS_FILE}.bak", POSTS_FILE)
                st.info("Restored previous version from backup")
            except Exception as restore_error:
                st.error(f"Error restoring backup: {restore_error}")

def process_media(uploaded_file):
    """Process uploaded media files"""
    if uploaded_file is None:
        return None
        
    file_type = uploaded_file.type
    
    if file_type.startswith('image'):
        return {
            'type': 'image',
            'data': uploaded_file.getvalue(),
            'mime': file_type
        }
    elif file_type.startswith('video'):
        return {
            'type': 'video',
            'data': uploaded_file.getvalue(),
            'mime': file_type
        }
    
    return None

def format_timestamp(timestamp):
    """Format timestamp in Instagram style"""
    now = datetime.now()
    post_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
    delta = now - post_time
    
    if delta.days > 7:
        return post_time.strftime("%B %d")
    elif delta.days > 0:
        return f"{delta.days}d"
    elif delta.seconds > 3600:
        return f"{delta.seconds // 3600}h"
    elif delta.seconds > 60:
        return f"{delta.seconds // 60}m"
    else:
        return "now"

def get_random_story_viewers():
    """Generate random story viewers"""
    num_users = len(SAMPLE_USERS)
    # Get a random number of viewers between 1 and the total number of users
    num_viewers = random.randint(1, num_users)
    return random.sample([u["username"] for u in SAMPLE_USERS], num_viewers)

# -----------------------------
# UI Components
# -----------------------------

def render_header():
    """Render clean, professional header"""
    st.markdown("""
        <div class="app-header">
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 1.5rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <h1 style="font-size: 1.5rem; margin: 0;">Community Feed</h1>
                    <span style="color: #666; font-size: 0.9rem;">Share • Connect • Engage</span>
                </div>
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <button style="background: none; border: none; color: #0095F6; cursor: pointer; padding: 0.5rem;">
                        <span style="font-size: 1.2rem;">✉️</span>
                    </button>
                    <button style="background: none; border: none; color: #0095F6; cursor: pointer; padding: 0.5rem;">
                        <span style="font-size: 1.2rem;">🔔</span>
                    </button>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_stories():
    """Render Instagram-like stories section"""
    st.markdown("""
        <div class="stories-container">
            <div style="text-align: center;">
                <div class="post-avatar" style="margin: 0 auto; position: relative;">
                    <span style="font-size: 20px;">➕</span>
                </div>
                <div style="color: #8e8e8e; font-size: 12px; margin-top: 4px;">Your story</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Simulate story viewers
    if random.random() > 0.7:  # 30% chance to show story views
        viewers = get_random_story_viewers()
        st.markdown(f"<div style='color: #8e8e8e; font-size: 12px; margin: 8px 16px;'>{len(viewers)} views • {', '.join(viewers[:3])}...</div>", unsafe_allow_html=True)

def render_post(post, current_user):
    """Render a single post card with responsive media"""
    user_info = next((u for u in SAMPLE_USERS if u["name"] == post["user"]), SAMPLE_USERS[-1])
    
    with st.container():
        # Start post block
        st.markdown(f"""
            <div class="post-block">
                <div class="post-container">
                    <div class="post-header">
                        <div class="post-avatar">{user_info["avatar"]}</div>
                        <div class="post-user-info">
                            <span class="post-username">{user_info["username"]}</span>
                            <span class="post-time">{format_timestamp(post["time"])}</span>
                        </div>
                        <div class="post-options">⋮</div>
                    </div>
                    <div class="post-wrapper">
        """, unsafe_allow_html=True)
        
        # Post content
        if post.get("message"):
            st.markdown(f'<div class="post-content">{post["message"]}</div>', unsafe_allow_html=True)
        
        # Media content
        if post.get("media"):
            media = post["media"]
            if media["type"] == "image":
                st.markdown("""
                    <div class="media-container">
                        <div class="media-wrapper">
                """, unsafe_allow_html=True)
                st.image(media["data"], use_column_width=True)
                st.markdown("</div></div>", unsafe_allow_html=True)
            elif media["type"] == "video":
                st.markdown("""
                    <div class="media-container">
                        <div class="media-wrapper wide">
                """, unsafe_allow_html=True)
                st.video(media["data"])
                st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Reactions section
        st.markdown('<div class="reactions-container">', unsafe_allow_html=True)
        cols = st.columns(len(REACTIONS))
        for i, (emoji, label) in enumerate(REACTIONS.items()):
            with cols[i]:
                users = post.get("reactions", {}).get(emoji, [])
                count = len(users)
                has_reacted = current_user in users
                button_class = "reaction-button active" if has_reacted else "reaction-button"
                
                if st.button(f"{emoji}", key=f"react_{post.get('id', '')}_{emoji}"):
                    if "reactions" not in post:
                        post["reactions"] = {}
                    if emoji not in post["reactions"]:
                        post["reactions"][emoji] = []
                    if current_user in post["reactions"][emoji]:
                        post["reactions"][emoji].remove(current_user)
                    else:
                        post["reactions"][emoji].append(current_user)
                    save_posts(st.session_state.posts)
                    st.rerun()
                
                if count > 0:
                    st.markdown(f"<div style='color: #8e8e8e; font-size: 12px;'>{count}</div>", unsafe_allow_html=True)
        
        # Comments section
        comments = post.get("comments", [])
        if comments:
            st.markdown(f"<div class='comment-stats'>{len(comments)} comments</div>", unsafe_allow_html=True)
            
            for comment in comments[:3]:  # Show only last 3 comments
                st.markdown(f"""
                    <div class="comment-card">
                        <div class="comment-content">
                            <span class="comment-username">{comment['user']}</span>
                            <span class="comment-text">{comment['text']}</span>
                            <div class="comment-time">{format_timestamp(comment['time'])}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Comment form
        with st.form(key=f"comment_form_{post.get('id', '')}"):
            comment_text = st.text_input("", placeholder="Add a comment...", key=f"comment_input_{post.get('id', '')}")
            if st.form_submit_button("Post"):
                if comment_text.strip():
                    if "comments" not in post:
                        post["comments"] = []
                    new_comment = {
                        "user": current_user,
                        "avatar": next(u["avatar"] for u in SAMPLE_USERS if u["name"] == current_user),
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "text": comment_text
                    }
                    post["comments"].append(new_comment)
                    save_posts(st.session_state.posts)
                    st.rerun()

def render_create_post():
    """Render create post form"""
    st.markdown("""
        <div style="background: #242424; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
            <h3 style="margin: 0 0 1.5rem 0; color: #fff; font-size: 1.2rem;">Create New Post</h3>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form(key="create_post"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            message = st.text_area("What's on your mind?", height=100, 
                                 placeholder="Share your thoughts, ideas, or updates...")
        
        with col2:
            user = st.selectbox("Post as", options=[u["name"] for u in SAMPLE_USERS])
        
        uploaded_file = st.file_uploader("Add photo or video", 
                                       type=["jpg", "jpeg", "png", "mp4"],
                                       help="Supported formats: JPG, PNG, MP4")
        
        col3, col4, col5 = st.columns([1, 1, 1])
        with col4:
            if st.form_submit_button("📤 Share Post", use_container_width=True):
                if message.strip() or uploaded_file:
                    media_data = process_media(uploaded_file)
                    new_post = {
                        "id": str(time.time()),
                        "user": user,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "message": message,
                        "media": media_data,
                        "reactions": {},
                        "comments": []
                    }
                    st.session_state.posts.insert(0, new_post)
                    save_posts(st.session_state.posts)
                    st.rerun()
                media_data = process_media(uploaded_file)
                new_post = {
                    "id": str(time.time()),
                    "user": user,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "message": message,
                    "media": media_data,
                    "reactions": {},
                    "comments": []
                }
                st.session_state.posts.insert(0, new_post)
                save_posts(st.session_state.posts)
                st.rerun()

# -----------------------------
# Main App
# -----------------------------

def main():
    # Initialize session state
    if "current_user" not in st.session_state:
        st.session_state.current_user = SAMPLE_USERS[0]["name"]
    if "posts" not in st.session_state:
        st.session_state.posts = load_posts()
    if "posts_to_show" not in st.session_state:
        st.session_state.posts_to_show = POSTS_PER_PAGE
        
    # Load custom CSS
    with open(Path(__file__).parent.parent / "styles" / "social.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # App layout
    render_header()
    
    # Navigation tabs
    tab1, tab2 = st.tabs(["📱 Feed", "✏️ Create Post"])
    
    with tab1:
        render_stories()
        
        # Display posts
        posts_to_display = st.session_state.posts[:st.session_state.posts_to_show]
        for post in posts_to_display:
            render_post(post, st.session_state.current_user)
        
        # Load more button
        if st.session_state.posts_to_show < len(st.session_state.posts):
            if st.button("Load More", key="load_more"):
                st.session_state.posts_to_show += POSTS_PER_PAGE
                st.rerun()
    
    with tab2:
        render_create_post()

if __name__ == "__main__":
    main()
