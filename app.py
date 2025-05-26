from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Database setup
DATABASE_URL=os.getenv("postgresql://postgres:QibNWtvOoUaVzZnrXVjlGeJBLmZTvNsl@postgres.railway.internal:5432/railway")
def init_db():
    conn = sqlite3.connect('contact.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET"])
def home():
    return "Backend running for portfolio", 200

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"error": "Missing required fields"}), 400

    conn = sqlite3.connect("contact.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, email, subject, message) VALUES (?, ?, ?, ?)",
        (name, email, subject, message)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Message received!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
