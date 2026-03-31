import threading
import time


class Counter:
    """A counter object to hold the counter value. Used to avoid global variables."""
    
    def __init__(self):
        """Initialize the counter to 0."""
        self.value = 0


def increment_without_lock(counter, thread_id, increments=1000):
    """
    Increment the counter without lock (demonstrates race condition).
    
    Args:
        counter: The Counter object to increment
        thread_id: The thread ID (for logging)
        increments: Number of times to increment (default 1000)
    """
    for _ in range(increments):
        # This is a race condition!
        # Read-modify-write is not atomic
        temp = counter.value
        # Add a tiny delay to increase chance of race condition
        time.sleep(0.0001)
        temp += 1
        counter.value = temp


def increment_with_lock(counter, lock, thread_id, increments=1000):
    """
    Increment the counter with lock (thread-safe).
    
    Args:
        counter: The Counter object to increment
        lock: The threading.Lock to ensure atomicity
        thread_id: The thread ID (for logging)
        increments: Number of times to increment (default 1000)
    """
    for _ in range(increments):
        with lock:  # Acquire lock before accessing shared resource
            counter.value += 1


def test_without_lock(num_threads=10, increments_per_thread=1000):
    """
    Test counter increment without lock.
    
    Args:
        num_threads: Number of threads to spawn
        increments_per_thread: How many times each thread increments
        
    Returns:
        The final counter value
    """
    counter = Counter()
    threads = []
    
    # Create and start threads
    for i in range(num_threads):
        thread = threading.Thread(
            target=increment_without_lock,
            args=(counter, i, increments_per_thread)
        )
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return counter.value


def test_with_lock(num_threads=10, increments_per_thread=1000):
    """
    Test counter increment with lock.
    
    Args:
        num_threads: Number of threads to spawn
        increments_per_thread: How many times each thread increments
        
    Returns:
        The final counter value
    """
    counter = Counter()
    lock = threading.Lock()
    threads = []
    
    # Create and start threads
    for i in range(num_threads):
        thread = threading.Thread(
            target=increment_with_lock,
            args=(counter, lock, i, increments_per_thread)
        )
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return counter.value


# Test code demonstrating race condition and its fix
if __name__ == "__main__":
    num_threads = 10
    increments = 1000
    expected = num_threads * increments
    
    print("=" * 60)
    print("RACE CONDITION DEMONSTRATION")
    print("=" * 60)
    print(f"\nThreads: {num_threads}")
    print(f"Increments per thread: {increments}")
    print(f"Expected final value: {expected}\n")
    
    # Test without lock - run multiple times to show inconsistency
    print("--- WITHOUT LOCK (Race Condition) ---")
    print("Running multiple times to show inconsistency:\n")
    
    results_without_lock = []
    for run in range(5):
        result = test_without_lock(num_threads, increments)
        results_without_lock.append(result)
        status = "✓ Correct" if result == expected else "✗ INCORRECT"
        print(f"Run {run + 1}: {result:5d} {status}")
    
    print(f"\nObservation: Results vary! Average: {sum(results_without_lock) / len(results_without_lock):.0f}")
    print(f"              Expected: {expected}, but got different values each run")
    
    # Test with lock - run multiple times to show consistency
    print("\n--- WITH LOCK (Thread-Safe) ---")
    print("Running multiple times to show consistency:\n")
    
    results_with_lock = []
    for run in range(5):
        result = test_with_lock(num_threads, increments)
        results_with_lock.append(result)
        status = "✓ Correct" if result == expected else "✗ INCORRECT"
        print(f"Run {run + 1}: {result:5d} {status}")
    
    print(f"\nObservation: Results are always correct! Every run produces {expected}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    without_lock_all_correct = all(v == expected for v in results_without_lock)
    with_lock_all_correct = all(v == expected for v in results_with_lock)
    
    print(f"\nWithout Lock:")
    print(f"  Correct results:   {sum(1 for v in results_without_lock if v == expected)}/{len(results_without_lock)}")
    print(f"  Min value:         {min(results_without_lock)}")
    print(f"  Max value:         {max(results_without_lock)}")
    print(f"  Lost increments:   {expected - min(results_without_lock)}")
    
    print(f"\nWith Lock:")
    print(f"  Correct results:   {sum(1 for v in results_with_lock if v == expected)}/{len(results_with_lock)}")
    print(f"  All values:        {results_with_lock[0]}")
    
    print("\n" + "=" * 60)
    print("WHY THE RACE CONDITION OCCURS")
    print("=" * 60)
    print("""
The read-modify-write operation is NOT atomic without a lock:

    counter.value += 1
    
Is actually:
    1. READ:   temp = counter.value        (Thread sees current value)
    2. MODIFY: temp = temp + 1             (Increment in Thread's memory)
    3. WRITE:  counter.value = temp        (Write back to shared counter)

Between any two steps, another thread might execute!

Example of Race Condition:
    Thread 1: READ counter.value (5)
    Thread 2: READ counter.value (5)        ← Both read the same value!
    Thread 1: WRITE counter.value (6)
    Thread 2: WRITE counter.value (6)       ← Both write the same result!
    
    Result: Counter is 6, but it should be 7!
    One increment was LOST due to the race condition.

SOLUTION: Use threading.Lock
    with lock:
        counter.value += 1
        
Now only ONE thread can execute the critical section at a time.
All operations are atomic and thread-safe.
    """)
