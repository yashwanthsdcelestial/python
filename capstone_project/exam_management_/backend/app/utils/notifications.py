import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings

logger = logging.getLogger(__name__)


def _send_email(to_email: str, subject: str, body_html: str) -> None:
    """Send an email using SMTP. Logs warning if SMTP not configured."""
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning(f"[EMAIL SKIPPED - SMTP not configured] To: {to_email} | Subject: {subject}")
        logger.info(f"Email body preview: {body_html[:200]}")
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        msg["To"] = to_email
        msg.attach(MIMEText(body_html, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAILS_FROM_EMAIL, to_email, msg.as_string())

        logger.info(f"Email sent to {to_email}: {subject}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")


def send_enrollment_notification(email: str, name: str, exam_title: str) -> None:
    subject = f"Enrolled in: {exam_title}"
    body = f"""
    <html><body>
    <h2>Enrollment Confirmed!</h2>
    <p>Hello <strong>{name}</strong>,</p>
    <p>You have been successfully enrolled in the exam: <strong>{exam_title}</strong>.</p>
    <p>Good luck with your exam!</p>
    <br><p>— Exam Portal Team</p>
    </body></html>
    """
    _send_email(email, subject, body)


def send_result_notification(
    email: str, name: str, exam_title: str,
    score: float, total: float, percentage: float, passed: bool
) -> None:
    result_word = "PASSED ✅" if passed else "FAILED ❌"
    subject = f"Result: {exam_title} — {result_word}"
    body = f"""
    <html><body>
    <h2>Exam Result</h2>
    <p>Hello <strong>{name}</strong>,</p>
    <p>Here are your results for <strong>{exam_title}</strong>:</p>
    <ul>
        <li>Score: {score}/{total}</li>
        <li>Percentage: {percentage}%</li>
        <li>Result: <strong>{result_word}</strong></li>
    </ul>
    <br><p>— Exam Portal Team</p>
    </body></html>
    """
    _send_email(email, subject, body)


def send_registration_welcome(email: str, name: str) -> None:
    subject = "Welcome to Exam Portal!"
    body = f"""
    <html><body>
    <h2>Welcome, {name}!</h2>
    <p>Your account has been created successfully on Exam Portal.</p>
    <p>You can now browse and enroll in available exams.</p>
    <br><p>— Exam Portal Team</p>
    </body></html>
    """
    _send_email(email, subject, body)
