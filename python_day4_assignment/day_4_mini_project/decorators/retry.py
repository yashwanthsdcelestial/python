import functools
import logging

logger = logging.getLogger(__name__)


def retry(max_attempts: int = 3):
    """Retries the decorated function up to max_attempts times on exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    print(f"[RETRY] Attempt {attempt}/{max_attempts} for '{func.__name__}' failed: {exc}")
                    logger.warning(
                        f"[RETRY] Attempt {attempt}/{max_attempts} for '{func.__name__}' failed: {exc}"
                    )
            raise last_exc
        return wrapper
    return decorator