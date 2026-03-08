from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from datetime import datetime
import uuid
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# In-memory store (replace with a real DB in production)
messages_store = {}
users_store = {
    "u1": {"id": "u1", "name": "Alex Morgan", "avatar": "AM", "status": "online", "color": "#6c63ff"},
    "u2": {"id": "u2", "name": "Jordan Lee", "avatar": "JL", "status": "online", "color": "#00d4aa"},
    "u3": {"id": "u3", "name": "Sam Rivera", "avatar": "SR", "status": "away", "color": "#ff6b6b"},
    "u4": {"id": "u4", "name": "Casey Kim", "avatar": "CK", "status": "offline", "color": "#ffa500"},
}
channels_store = {
    "c1": {"id": "c1", "name": "General", "description": "General discussion", "members": ["u1","u2","u3","u4"], "type": "channel"},
    "c2": {"id": "c2", "name": "Design", "description": "Design assets & feedback", "members": ["u1","u2"], "type": "channel"},
    "c3": {"id": "c3", "name": "Engineering", "description": "Tech talk", "members": ["u1","u3","u4"], "type": "channel"},
}

# Seed some messages
seed_messages = [
    {"id": str(uuid.uuid4()), "channel_id": "c1", "user_id": "u2", "text": "Hey everyone! Just pushed the new design updates 🎨", "timestamp": "2025-01-15T09:00:00"},
    {"id": str(uuid.uuid4()), "channel_id": "c1", "user_id": "u3", "text": "Looks amazing! The new color palette is 🔥", "timestamp": "2025-01-15T09:02:00"},
    {"id": str(uuid.uuid4()), "channel_id": "c1", "user_id": "u1", "text": "Shipping the v2.0 release tonight. Stay tuned!", "timestamp": "2025-01-15T09:05:00"},
    {"id": str(uuid.uuid4()), "channel_id": "c2", "user_id": "u2", "text": "Uploading the Figma files now", "timestamp": "2025-01-15T08:00:00"},
    {"id": str(uuid.uuid4()), "channel_id": "c3", "user_id": "u4", "text": "CI/CD pipeline is green ✅", "timestamp": "2025-01-15T08:30:00"},
]
for msg in seed_messages:
    cid = msg["channel_id"]
    if cid not in messages_store:
        messages_store[cid] = []
    messages_store[cid].append(msg)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/me")
def get_me():
    return jsonify(users_store["u1"])


@app.route("/api/users")
def get_users():
    return jsonify(list(users_store.values()))


@app.route("/api/channels")
def get_channels():
    return jsonify(list(channels_store.values()))


@app.route("/api/channels/<channel_id>/messages")
def get_messages(channel_id):
    msgs = messages_store.get(channel_id, [])
    enriched = []
    for m in msgs:
        enriched.append({**m, "user": users_store.get(m["user_id"], {})})
    return jsonify(enriched)


@app.route("/api/channels/<channel_id>/messages", methods=["POST"])
def send_message(channel_id):
    data = request.json
    msg = {
        "id": str(uuid.uuid4()),
        "channel_id": channel_id,
        "user_id": data.get("user_id", "u1"),
        "text": data.get("text", "").strip(),
        "timestamp": datetime.utcnow().isoformat(),
    }
    if not msg["text"]:
        return jsonify({"error": "empty message"}), 400
    if channel_id not in messages_store:
        messages_store[channel_id] = []
    messages_store[channel_id].append(msg)
    return jsonify({**msg, "user": users_store.get(msg["user_id"], {})})


@app.route("/api/channels/<channel_id>/messages/<message_id>", methods=["DELETE"])
def delete_message(channel_id, message_id):
    msgs = messages_store.get(channel_id, [])
    messages_store[channel_id] = [m for m in msgs if m["id"] != message_id]
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
