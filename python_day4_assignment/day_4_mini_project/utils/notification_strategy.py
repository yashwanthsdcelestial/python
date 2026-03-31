"""
OCP-compliant notification strategy system.
Adding a new channel (e.g. EmailNotification) requires only a new subclass —
no changes to existing code.
"""
from abc import ABC, abstractmethod
import logging

notif_logger = logging.getLogger("notifications")


class NotificationStrategy(ABC):
    """Abstract base: every notification channel implements send()."""

    @abstractmethod
    def send(self, loan_id: int, username: str, status: str) -> None:
        ...


class ConsoleNotification(NotificationStrategy):
    def send(self, loan_id: int, username: str, status: str) -> None:
        print(f"[CONSOLE] Loan #{loan_id} for '{username}' → {status}")


class LogFileNotification(NotificationStrategy):
    def send(self, loan_id: int, username: str, status: str) -> None:
        notif_logger.info(f"[LOG] Loan #{loan_id} for '{username}' → {status}")


class EmailNotification(NotificationStrategy):
    """Future channel — adding this does NOT change ConsoleNotification or LogFileNotification."""
    def send(self, loan_id: int, username: str, status: str) -> None:
        notif_logger.info(f"[EMAIL] Would send email to '{username}' re: Loan #{loan_id} → {status}")


class NotificationDispatcher:
    """Holds a list of strategies and broadcasts to all of them."""

    def __init__(self, strategies: list[NotificationStrategy]):
        self._strategies = strategies

    def notify(self, loan_id: int, username: str, status: str) -> None:
        for strategy in self._strategies:
            strategy.send(loan_id, username, status)


# Default dispatcher used by the app
default_dispatcher = NotificationDispatcher([
    ConsoleNotification(),
    LogFileNotification(),
])