# Pulse Chat App

A professional, dark-themed real-time chat web app inspired by Slack, Discord, and Notion.

## Stack
- **Backend**: Python + Flask + Flask-CORS
- **Frontend**: Pure HTML, CSS, JavaScript (no framework)
- **Design**: Syne + DM Sans fonts, dark obsidian theme

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the Flask server
python app.py

# 3. Open your browser at
http://localhost:5000
```

## Features
- 🏗️ Multi-channel sidebar navigation
- 💬 Real-time-style messaging (3s polling)
- 🗑️ Delete your own messages
- 👥 Members panel per channel
- 🟢 User status indicators (online / away / offline)
- ✨ Optimistic UI updates
- 📱 Responsive layout
- 🎨 Premium dark UI — Uber/Spotify/Apple aesthetic

## Project Structure
```
pulse-chat/
├── app.py              # Flask backend (REST API)
├── requirements.txt
└── templates/
    └── index.html      # Full frontend (HTML + CSS + JS)
```

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/me | Current user info |
| GET | /api/users | All users |
| GET | /api/channels | All channels |
| GET | /api/channels/:id/messages | Get messages |
| POST | /api/channels/:id/messages | Send a message |
| DELETE | /api/channels/:id/messages/:msgId | Delete a message |
