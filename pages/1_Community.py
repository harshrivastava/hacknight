"""
Community Discussion Page — Naborly
Allows users to post messages with media attachments, reactions, and comments
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from PIL import Image
import io
from pathlib import Path

# Initialize session state for current user
if "current_user" not in st.session_state:
    st.session_state.current_user = "Guest User"

# -----------------------------
# Constants and Data
# -----------------------------

# File to store posts (simple JSON persistence)
POSTS_FILE = "community_posts.json"

# Dummy user data (in a real app, this would come from authentication)
SAMPLE_USERS = [
    {"name": "Neha Singh", "avatar": "👩"},
    {"name": "Amit Kumar", "avatar": "👨"},
    {"name": "Saira Khan", "avatar": "👩"},
    {"name": "Guest User", "avatar": "👤"}
]

# -----------------------------
# Helper Functions
# -----------------------------

def load_posts():
    """Load posts from JSON file or return default posts if file doesn't exist"""
    try:
        if os.path.exists(POSTS_FILE):
            with open(POSTS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading posts: {e}")
    
    # Default posts if file doesn't exist
    return [
        {
            "id": "1",
            "user": "Neha Singh",
            "avatar": "👩",
            "time": "2025-10-31 14:20",
            "message": "Looking for recommendations for a good tutor in our area. My daughter needs help with Grade 8 mathematics.",
            "media": None,
            "reactions": {
                "👍": ["Amit Kumar", "Saira Khan"],
                "❤️": ["Raj Verma"],
                "🙏": ["Guest User"]
            },
            "comments": [
                {
                    "user": "Saira Khan",
                    "avatar": "👩",
                    "time": "2025-10-31 14:25",
                    "text": "I know a great math tutor! Will DM you the details."
                },
                {
                    "user": "Raj Verma",
                    "avatar": "👨",
                    "time": "2025-10-31 14:30",
                    "text": "My daughter goes to ABC Tutorials near the community hall. They're very good!"
                }
            ]
        },
        {
            "id": "2",
            "user": "Amit Kumar",
            "avatar": "👨",
            "time": "2025-10-31 13:05",
            "message": "Found this beautiful sunset view from our community park!",
            "media": None,
            "reactions": {
                "👍": ["Neha Singh"],
                "❤️": ["Saira Khan", "Guest User"],
                "🌟": ["Raj Verma"]
            },
            "comments": [
                {
                    "user": "Saira Khan",
                    "avatar": "👩",
                    "time": "2025-10-31 13:10",
                    "text": "Beautiful! We're so lucky to have this park in our ward."
                }
            ]
        }
    ]

def save_posts(posts):
    """Save posts to JSON file"""
    try:
        with open(POSTS_FILE, 'w') as f:
            json.dump(posts, f)
    except Exception as e:
        st.error(f"Error saving posts: {e}")

def process_uploaded_media(uploaded_file):
    """Process an uploaded media file and return it in a format suitable for display"""
    if uploaded_file is None:
        return None
        
    # Get file info
    file_type = uploaded_file.type
    
    if file_type.startswith('image'):
        # For images, we'll return the bytes for display
        return {
            'type': 'image',
            'data': uploaded_file.getvalue(),
            'mime': file_type
        }
    elif file_type.startswith('video'):
        # For videos, we'll use Streamlit's native video support
        return {
            'type': 'video',
            'data': uploaded_file.getvalue(),
            'mime': file_type
        }
    
    return None

# -----------------------------
# Page Layout
# -----------------------------

st.title("Community Discussion")
st.write("Share updates, questions, and media with your neighbors!")

# Initialize session state for posts if not exists
if 'posts' not in st.session_state:
    st.session_state.posts = load_posts()

# Post creation form
with st.form(key='create_post'):
    st.write("### Create a New Post")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        message = st.text_area("What's on your mind?", height=100)
    with col2:
        # Simulated user selection (in a real app, this would come from auth)
        user = st.selectbox("Post as:", options=[u["name"] for u in SAMPLE_USERS])
        avatar = next(u["avatar"] for u in SAMPLE_USERS if u["name"] == user)

    uploaded_file = st.file_uploader("Add a photo or video", type=['png', 'jpg', 'jpeg', 'mp4'])
    
    submit = st.form_submit_button("Post")
    
    if submit and message.strip():
        # Process the post
        media_data = process_uploaded_media(uploaded_file)
        
        new_post = {
            "user": user,
            "avatar": avatar,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "message": message,
            "media": media_data
        }
        
        # Add to start of posts list
        st.session_state.posts.insert(0, new_post)
        save_posts(st.session_state.posts)
        st.rerun()  # Refresh to show new post

# Load social styles
with open(Path(__file__).parent.parent / "styles" / "social.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Display posts
st.write("### Recent Posts")

# Available reactions with labels
REACTIONS = {
    "👍": "Like",
    "❤️": "Love",
    "🌟": "Star",
    "🙏": "Thanks",
    "😊": "Smile"
}

for post in st.session_state.posts:
    with st.container():
        # Post container with modern card style
        st.markdown(f"""
            <div class="post-card animate-fade-in">
                <div class="post-header">
                    <span class="post-avatar">{post["avatar"]}</span>
                    <span>
                        <span class="post-user">{post["user"]}</span>
                        <span class="post-time">· {post["time"]}</span>
                    </span>
                </div>
        """, unsafe_allow_html=True)
        
        # Post header with user info
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            st.write(post["avatar"])
        with col2:
            st.write(f"**{post['user']}** · {post['time']}")
        
        # Post content
        st.markdown(f'<div class="post-content">{post["message"]}</div>', unsafe_allow_html=True)
        
        # Display media if present
        if post.get("media"):
            media = post["media"]
            if media["type"] == "image":
                st.image(media["data"], use_column_width=True)
            elif media["type"] == "video":
                st.video(media["data"])
        
        # Reactions section
        st.markdown('<div class="reactions-container">', unsafe_allow_html=True)
        
        # Get current user
        current_user = st.session_state.get("current_user", SAMPLE_USERS[0]["name"])
        
        # Show reaction buttons with counts
        cols = st.columns(len(REACTIONS))
        for i, (emoji, label) in enumerate(REACTIONS.items()):
            with cols[i]:
                users = post.get("reactions", {}).get(emoji, [])
                has_reacted = current_user in users
                count = len(users)
                
                # Create a button with dynamic styling based on reaction state
                button_class = "reaction-badge active" if has_reacted else "reaction-badge"
                st.markdown(
                    f'''<div class="{button_class}" title="{label}">
                        {emoji} <span class="reaction-count">{count if count > 0 else ''}</span>
                    </div>''',
                    unsafe_allow_html=True
                )
                
                # Button with different style based on whether user has reacted
                button_style = "background-color: #e5e7eb;" if has_reacted else "background-color: transparent;"
                if st.button(
                    emoji,
                    key=f"react_{post['id']}_{emoji}",
                    help="Click to react to this post"
                ):
                    # Initialize reactions dict if needed
                    if "reactions" not in post:
                        post["reactions"] = {}
                    if emoji not in post["reactions"]:
                        post["reactions"][emoji] = []
                    
                    # Toggle reaction
                    if current_user in post["reactions"][emoji]:
                        post["reactions"][emoji].remove(current_user)
                    else:
                        post["reactions"][emoji].append(current_user)
                    
                    # Save updated posts
                    save_posts(st.session_state.posts)
                    st.rerun()
        
        # Comments section
        comment_count = len(post.get("comments", []))
        st.markdown(
            f'''<div class="comments-section">
                <div class="comments-header">
                    💬 {comment_count} Comment{"s" if comment_count != 1 else ""}
                </div>
            ''',
            unsafe_allow_html=True
        )
        
        # Show existing comments
        for comment in post.get("comments", []):
            st.markdown(
                f"""
                <div class="comment-card">
                    <div class="comment-header">
                        <span class="comment-avatar">{comment['avatar']}</span>
                        <span class="comment-user">{comment['user']}</span>
                        <span class="comment-time">· {comment['time']}</span>
                    </div>
                    <div class="comment-text">{comment['text']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Add new comment
        st.markdown('<div class="comment-form">', unsafe_allow_html=True)
        comment_text = st.text_area(
            "",
            key=f"comment_{post['id']}",
            placeholder="Write a comment...",
            height=100
        )
        
        col1, col2, *_ = st.columns([0.2, 0.8])
        with col1:
            if st.button("💬 Comment", key=f"submit_comment_{post['id']}", type="primary"):
                if comment_text.strip():
                    # Initialize comments list if needed
                    if "comments" not in post:
                        post["comments"] = []
                    
                    # Add new comment
                    new_comment = {
                        "user": st.session_state.get("current_user", SAMPLE_USERS[0]["name"]),
                        "avatar": next(u["avatar"] for u in SAMPLE_USERS if u["name"] == st.session_state.get("current_user", SAMPLE_USERS[0]["name"])),
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "text": comment_text
                    }
                    post["comments"].append(new_comment)
                    
                    # Save updated posts
                    save_posts(st.session_state.posts)
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close comment form
        st.markdown('</div>', unsafe_allow_html=True)  # Close comments section
        st.markdown('</div>', unsafe_allow_html=True)  # Close post container

# Small helper text at bottom
st.caption("Posts are saved locally and will persist between sessions. Media uploads are for demonstration only.")