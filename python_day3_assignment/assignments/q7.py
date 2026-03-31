from q4 import SessionLocal
from q5 import User, Task
from sqlalchemy import desc, asc

def get_tasks_by_status(session, status):
    return session.query(Task).filter_by(status=status).all()

def get_tasks_sorted(session, sort_by, order="asc"):
    column = getattr(Task, sort_by) 
    if order == "desc":
        return session.query(Task).order_by(desc(column)).all()
    else:
        return session.query(Task).order_by(asc(column)).all()

def get_tasks_paginated(session, page=1, limit=10):
    offset_val = (page - 1) * limit
    return session.query(Task).offset(offset_val).limit(limit).all()

def get_user_with_tasks(session, username):
    return session.query(User).filter_by(name=username).first()

if __name__ == "__main__":
    session = SessionLocal()

    try:
        # 🔹 Filter by status
        pending = get_tasks_by_status(session, "pending")
        print(f"Pending tasks: {len(pending)}")
        for t in pending:
            print(f" - {t.title} ({t.owner.name})")

        # 🔹 Sorted
        sorted_tasks = get_tasks_sorted(session, sort_by="created_at", order="desc")
        print(f"\nSorted (newest first): {[t.title for t in sorted_tasks]}")

        # 🔹 Paginated
        page = get_tasks_paginated(session, page=1, limit=2)
        print(f"\nPage 1 (limit 2): {[t.title for t in page]}")

        # 🔹 User with tasks
        user = get_user_with_tasks(session, "alice")
        if user:
            print(f"\n{user.name}'s tasks:")
            for t in user.tasks:
                print(f" - {t.title} ({t.status})")
        else:
            print("\nUser not found")

    except Exception as e:
        print("Error:", e)

    finally:
        session.close()
        print("\nSession closed.")