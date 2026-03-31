import time
import functools
import logging

logger = logging.getLogger(__name__)


def timer(func):
    """Measures and logs execution time of the decorated function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"[TIMER] {func.__qualname__} took {elapsed:.4f}s")
        return result
    return wrapper