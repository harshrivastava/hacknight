# Naborly — Modern Community Social Platform

A full-featured local social platform built with Python, Streamlit, and SQLite, designed to connect neighbors and share community information.

## 🌟 Features

### Community Feed
- Instagram-style post feed with media support
- Reactions and comments on posts
- Real-time updates
- Media upload support (images and videos)
- Modern UI with animations and responsive design

### User Management
- User profiles with avatars and bios
- Login/signup functionality
- Session management
- Secure password handling

### Government Services
- Ration rates tracking
- Community announcements
- Local utility schedules

### Maps & Directory
- Interactive local area map
- Business directory
- Community services listing
- Points of interest

### Data Persistence
- SQLite database for reliable data storage
- Structured tables for:
  - Users and profiles
  - Posts and media
  - Comments and reactions
  - Ration rates
  - Notifications

## 🔧 Technology Stack

- **Frontend**: Streamlit
- **Database**: SQLite3
- **Styling**: Custom CSS
- **Media Handling**: PIL, IO
- **Data Format**: JSON, SQLite
- **Version Control**: Git

## 📁 Project Structure

```
hacknight/
├── Home.py                 # Main landing page
├── naborly_app.py          # Core application setup
├── setup_db.py            # Database initialization
├── README.md              # Documentation
├── requirements.txt       # Python dependencies
├── pages/
│   ├── 1_Community.py    # Community feed page
│   ├── 2_Ration_Rates.py # Government rates page
│   └── 3_Profile.py      # User profile page
├── styles/
│   ├── main.css          # Global styles
│   ├── modern.css        # Modern UI components
│   └── social.css        # Social feed styling
├── utils/
│   ├── auth.py           # Authentication helpers
│   ├── db.py            # Database operations
│   ├── db_helpers.py    # High-level DB functions
│   └── ui.py            # UI components
└── naborly.db           # SQLite database
```

## 🚀 Getting Started

1. **Prerequisites**
   - Python 3.7+
   - Git (optional)

2. **Installation**
   ```powershell
   # Clone the repository (or download ZIP)
   git clone https://github.com/yourusername/hacknight.git
   cd hacknight

   # Install requirements
   pip install -r requirements.txt

   # Initialize the database
   python setup_db.py
   ```

3. **Run the Application**
   ```powershell
   streamlit run Home.py
   ```

## 💾 Database Schema

The application uses SQLite with the following structure:

- **users**: User profiles and authentication
  ```sql
  CREATE TABLE users (
      id TEXT PRIMARY KEY,
      username TEXT UNIQUE NOT NULL,
      name TEXT NOT NULL,
      avatar TEXT,
      bio TEXT,
      followers INTEGER DEFAULT 0,
      following INTEGER DEFAULT 0,
      password_hash TEXT
  );
  ```

- **posts**: Community feed posts
  ```sql
  CREATE TABLE posts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id TEXT NOT NULL,
      message TEXT,
      media_type TEXT,
      media_url TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(user_id) REFERENCES users(id)
  );
  ```

- **comments**: Post comments
  ```sql
  CREATE TABLE comments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      post_id INTEGER NOT NULL,
      user_id TEXT NOT NULL,
      text TEXT NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(post_id) REFERENCES posts(id),
      FOREIGN KEY(user_id) REFERENCES users(id)
  );
  ```

- **reactions**: Post reactions/likes
  ```sql
  CREATE TABLE reactions (
      post_id INTEGER NOT NULL,
      user_id TEXT NOT NULL,
      emoji TEXT NOT NULL,
      FOREIGN KEY(post_id) REFERENCES posts(id),
      FOREIGN KEY(user_id) REFERENCES users(id),
      PRIMARY KEY(post_id, user_id, emoji)
  );
  ```

## 🎨 Features & Screenshots

### Modern UI Components
- Responsive post cards with hover effects
- Instagram-style story circles
- Clean, modern styling
- Animated transitions
- Mobile-friendly design

### Social Features
- Create posts with text and media
- React with emojis
- Comment on posts
- View user profiles
- Follow other users

### Government Integration
- Track ration rates
- View community announcements
- Access utility schedules
- Find local services

## 🔄 Recent Updates

- Added SQLite database integration
- Implemented user authentication
- Added profile management
- Enhanced UI with modern styling
- Added media upload support
- Improved post interactions

## 🛠️ Development Notes

### Database Connections
The app uses a connection pool pattern with SQLite:
```python
@st.cache_resource
def get_db_connection():
    return sqlite3.connect('naborly.db', check_same_thread=False)
```

### Media Handling
Media files are currently stored in the database but can be easily modified to use file system or cloud storage by updating the relevant handlers in `db_helpers.py`.

### Authentication
User authentication is handled securely with password hashing and session management. Default test accounts are created during database initialization.

## 📝 Todo & Future Improvements

- [ ] Add search functionality
- [ ] Implement user following system
- [ ] Add direct messaging
- [ ] Enhance media handling with cloud storage
- [ ] Add post categories and tags
- [ ] Implement notification system
- [ ] Add user settings page
- [ ] Enhanced security features

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
