import random
import string
import sqlite3
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

consultation_api = Blueprint('consultation_api', __name__, url_prefix='/consultation')
api = Api(consultation_api)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('consultation.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            role TEXT NOT NULL,
            room_code TEXT NOT NULL,
            timestamp REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def generate_room_code():
    while True:
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        conn = sqlite3.connect('consultation.db')
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM consultation WHERE room_code = ?', (room_code,))
        if not cursor.fetchone():
            conn.close()
            return room_code
        conn.close()

def cleanup_old_entries():
    current_time = datetime.now().timestamp()
    expiration_time = 3600  # 1 hour
    with sqlite3.connect('consultation.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM consultation WHERE timestamp < ?', (current_time - expiration_time,))
        conn.commit()

def add_timestamp_column():
    with sqlite3.connect('consultation.db') as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(consultation)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'timestamp' not in columns:
            cursor.execute('ALTER TABLE consultation ADD COLUMN timestamp REAL')
            conn.commit()

# Initialize the database and add the timestamp column if it doesn't exist
init_db()
add_timestamp_column()

class Consultation(Resource):
    class Consultation_Create_Server(Resource):
        def post(self):
            cleanup_old_entries()
            room_code = generate_room_code()
            username = request.json.get('username')
            timestamp = datetime.now().timestamp()
            conn = sqlite3.connect('consultation.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO consultation (username, role, room_code, timestamp) VALUES (?, ?, ?, ?)', (username, 'creator', room_code, timestamp))
            conn.commit()
            cursor.execute('SELECT username FROM consultation WHERE room_code = ?', (room_code,))
            users = cursor.fetchall()
            conn.close()
            return jsonify({
                "message": "Consultation server created",
                "room_code": room_code,
                "users": list(set(user[0] for user in users))
            })

    class Consultation_Join_Server(Resource):
        def post(self):
            cleanup_old_entries()
            room_code = request.json.get('roomCode')
            username = request.json.get('username')
            timestamp = datetime.now().timestamp()
            conn = sqlite3.connect('consultation.db')
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM consultation WHERE room_code = ?', (room_code,))
            if cursor.fetchone():
                cursor.execute('INSERT INTO consultation (username, role, room_code, timestamp) VALUES (?, ?, ?, ?)', (username, 'participant', room_code, timestamp))
                conn.commit()
                cursor.execute('SELECT username FROM consultation WHERE room_code = ?', (room_code,))
                users = cursor.fetchall()
                conn.close()
                return jsonify({
                    "message": "Joined room successfully",
                    "room_code": room_code,
                    "users": list(set(user[0] for user in users))
                })
            else:
                conn.close()
                return jsonify({"message": "Room not found"}), 404

    class Consultation_Users(Resource):
        def get(self):
            cleanup_old_entries()
            room_code = request.args.get('roomCode')
            conn = sqlite3.connect('consultation.db')
            cursor = conn.cursor()
            cursor.execute('SELECT username FROM consultation WHERE room_code = ?', (room_code,))
            users = cursor.fetchall()
            conn.close()
            if users:
                return jsonify({
                    "room_code": room_code,
                    "users": list(set(user[0] for user in users))
                })
            else:
                return jsonify({"message": "Room not found"}), 404

    class Consultation_Leave_Server(Resource):
        def post(self):
            cleanup_old_entries()
            room_code = request.json.get('roomCode')
            username = request.json.get('username')
            conn = sqlite3.connect('consultation.db')
            cursor = conn.cursor()
            cursor.execute('SELECT role FROM consultation WHERE room_code = ? AND username = ?', (room_code, username))
            role = cursor.fetchone()
            if role:
                if role[0] == 'creator':
                    cursor.execute('DELETE FROM consultation WHERE room_code = ?', (room_code,))
                    message = "Room and all users deleted successfully"
                else:
                    cursor.execute('DELETE FROM consultation WHERE room_code = ? AND username = ?', (room_code, username))
                    message = "Left room successfully"
                conn.commit()
                conn.close()
                return jsonify({"message": message})
            else:
                conn.close()
                return jsonify({"message": "User not found in room"}), 404

    api.add_resource(Consultation_Create_Server, '/create')
    api.add_resource(Consultation_Join_Server, '/join')
    api.add_resource(Consultation_Users, '/users')
    api.add_resource(Consultation_Leave_Server, '/leave')