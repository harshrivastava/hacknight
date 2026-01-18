# `Naborly`

> *A modern community social platform built with Python, Streamlit, and SQLite*

[![Live Demo](https://img.shields.io/badge/Live_Demo-Visit_App-blue?style=for-the-badge&logo=streamlit)](https://naborly.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-3-green?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)

<div align="center">
  <h3><code>Connecting Neighbors, Building Community</code></h3>
</div>

## `🌟 Features`

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

## `🚀 Quick Start`

<details>
<summary><code>Prerequisites</code></summary>

```bash
Python 3.7+
Git (optional)
```

</details>

<details>
<summary><code>Local Setup</code></summary>

```bash
# Clone the repository
git clone https://github.com/harshrivastava/naborly.git

# Navigate to project directory
cd naborly

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python setup_db.py

# Launch application
streamlit run Home.py
```

</details>

<details>
<summary><code>Access the App</code></summary>

```bash
Local: http://localhost:8501
Network: http://YOUR_IP:8501
Live: https://naborly.streamlit.app/
```

</details>

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

## `📸 Screenshots`

<details>
<summary><code>Click to view application screenshots</code></summary>

![Screenshot](Screenshot%20(40).png)

</details>

## `👥 Contributors`

This project exists thanks to all the people who contribute:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/harshrivastava">
        <img src="https://github.com/harshrivastava.png" width="100px;" alt="Harsh Rivastava"/><br />
        <sub><code>Harsh Shrivastava</code></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Codexphere19">
        <img src="https://github.com/Codexphere19.png" width="100px;" alt="Devansh Lakhera"/><br />
        <sub><code>Devansh Lakhera</code></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/himanjhi07">
        <img src="https://github.com/himanjhi07.png" width="100px;" alt="Himanshu Manjhi"/><br />
        <sub><code>Himanshu Manjhi</code></sub>
      </a>
    </td>
  </tr>
</table>

## `📝 Todo & Future Improvements`

```md
◻️ Add search functionality
◻️ Implement user following system
◻️ Add direct messaging
◻️ Enhance media handling with cloud storage
◻️ Add post categories and tags
◻️ Implement notification system
◻️ Add user settings page
◻️ Enhanced security features
```

## `🔗 Live Demo`

Experience Naborly in action at [naborly.streamlit.app](https://naborly.streamlit.app/)

## `🤝 Contributing`

```bash
1. Fork the repository
2. Create your feature branch: git checkout -b feature/amazing-feature
3. Commit your changes: git commit -m 'Add amazing feature'
4. Push to the branch: git push origin feature/amazing-feature
5. Open a Pull Request
```

## `📄 License`

```
MIT License
Copyright (c) 2025 Naborly Team
```
