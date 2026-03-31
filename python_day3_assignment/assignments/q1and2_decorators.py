import time
import random
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[timer] {func.__name__} executed in {end - start:.4f}s")
        return result
    return wrapper

@timer
def compute_squares(n):
    return sum(i * i for i in range(1, n + 1))

def retry(max_attempts):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    print(f"[retry] Attempt {attempt} succeeded!")
                    return result
                except Exception as e:
                    print(f"[retry] Attempt {attempt} failed: {e}")
                    if attempt == max_attempts:
                        raise Exception(f"All {max_attempts} attempts failed")
        return wrapper
    return decorator

random.seed(42)

@retry(max_attempts=5)
def fetch_data():
    if random.choice([True, False]):
        raise ConnectionError("Server unreachable")
    return {"status": "ok"}

if __name__ == "__main__":
    print("Squares result:", compute_squares(10000))
    
    print("\nFetching data...")
    result = fetch_data()
    print("Final result:", result)