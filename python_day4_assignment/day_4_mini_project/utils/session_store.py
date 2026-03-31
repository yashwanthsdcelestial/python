# utils/session_store.py

from uuid import uuid4

sessions = {}


def create_session(user_id: int, username: str, role: str) -> str:
    session_id = str(uuid4())
    sessions[session_id] = {
        "user_id": user_id,
        "username": username,
        "role": role
    }
    return session_id


def get_session(session_id: str):
    return sessions.get(session_id)


def delete_session(session_id: str):
    sessions.pop(session_id, None)