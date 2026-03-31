# utils/notifications.py

from datetime import datetime


def _log_event(event: str, message: str):
    """Generic logger for all notification events."""
    print(f"[{datetime.now()}] [{event}] {message}")


# ── Loan Application Events ─────────────────────────────────────

def log_new_application(user_id: int, loan_id: int):
    _log_event(
        "NEW_APPLICATION",
        f"User {user_id} applied for Loan {loan_id}"
    )


def log_loan_approved(loan_id: int, approved_by: int):
    _log_event(
        "LOAN_APPROVED",
        f"Loan {loan_id} approved by Admin {approved_by}"
    )


def log_loan_rejected(loan_id: int, rejected_by: int):
    _log_event(
        "LOAN_REJECTED",
        f"Loan {loan_id} rejected by Admin {rejected_by}"
    )


# ── Review Notification (THIS FIXES YOUR CURRENT ERROR) ─────────

def send_review_notification(user_id: int, loan_id: int, status: str):
    _log_event(
        "REVIEW_NOTIFICATION",
        f"User {user_id} | Loan {loan_id} | Status: {status}"
    )


# ── User Events ─────────────────────────────────────────────────

def log_user_registered(user_id: int):
    _log_event(
        "USER_REGISTERED",
        f"New user registered with ID {user_id}"
    )


def log_user_login(user_id: int):
    _log_event(
        "USER_LOGIN",
        f"User {user_id} logged in"
    )


# ── Generic Logs ────────────────────────────────────────────────

def log_info(message: str):
    _log_event("INFO", message)


def log_error(message: str):
    _log_event("ERROR", message)