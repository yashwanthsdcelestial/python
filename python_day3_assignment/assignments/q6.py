from q4 import SessionLocal
from q5 import User

# ✅ NO import from crud

def create_user(session, username, email, password):
    user = User(name=username, email=email, encrypted_password=password)
    session.add(user)
    session.commit()
    return f"User '{username}' created with id {user.id}"

def get_all_users(session):
    return session.query(User).all()

def update_user_email(session, username, new_email):
    user = session.query(User).filter_by(name=username).first()
    if not user:
        raise ValueError(f"User '{username}' not found")
    user.email = new_email
    session.commit()
    return f"Updated {username}'s email to {new_email}"

def delete_user(session, username):
    user = session.query(User).filter_by(name=username).first()
    if not user:
        raise ValueError(f"User '{username}' not found")
    session.delete(user)
    session.commit()
    return f"User '{username}' deleted successfully"

if __name__ == "__main__":
    session = SessionLocal()

    try:
        print(create_user(session, "charlie", "charlie@mail.com", "pass1234"))

        users = get_all_users(session)
        print("\nAll Users:")
        for u in users:
            print(u)

        print(update_user_email(session, "charlie", "charlie.new@mail.com"))

        print(delete_user(session, "charlie"))

    except Exception as e:
        print("Error:", e)

    finally:
        session.close()
        print("Session closed.")