from q4 import SessionLocal
from q5 import User, Task
from sqlalchemy.exc import IntegrityError

def create_user_with_tasks(session, username, email, password, task_titles):
    try:
        user = User(name=username, email=email, encrypted_password=password)
        session.add(user)
        session.flush()  # Get user.id

        for title in task_titles:
            task = Task(title=title, owner_id=user.id)
            session.add(task)

        session.commit()
        return f"Transaction successful: User '{username}' created with {len(task_titles)} tasks"
    except IntegrityError as e:
        session.rollback()
        error_msg = str(e).split('\n')[0]  # Get the main error
        return f"Transaction rolled back: {error_msg}\n{email} was NOT saved"
    except Exception as e:
        session.rollback()
        return f"Transaction rolled back: {e}"

# Demonstration
if __name__ == "__main__":
    session = SessionLocal()

    # Case 1: Success
    print("--- Case 1: New user ---")
    result = create_user_with_tasks(session, "dave", "dave@mail.com", "pass1234",
    ["Setup environment", "Read documentation", "Complete onboarding"])
    print(result)

    # Case 2: Failure (duplicate username)
    print("\n--- Case 2: Duplicate user ---")
    result = create_user_with_tasks(session, "dave", "dave2@mail.com", "pass5678",
    ["Task A", "Task B", "Task C"])
    print(result)

    # Verify: dave should still have only 3 tasks (not 6)
    user = session.query(User).filter_by(name="dave").first()
    if user:
        print(f"\ndave's total tasks: {len(user.tasks)}")

    session.close()