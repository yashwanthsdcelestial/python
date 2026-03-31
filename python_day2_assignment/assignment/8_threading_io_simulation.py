import time
import threading
from concurrent.futures import ThreadPoolExecutor


def fetch_data(source, delay):
    """
    Simulate fetching data from an API.
    
    Args:
        source: The data source name
        delay: The simulated API delay in seconds
    """
    print(f"[START] Fetching from {source}...")
    time.sleep(delay)  # Simulate API call
    print(f"[END] Fetching from {source} (took {delay}s)")
    return {"source": source, "data": f"Data from {source}"}


def run_sequential(sources):
    """
    Run all fetch operations sequentially.
    
    Args:
        sources: List of tuples (source_name, delay)
        
    Returns:
        The total execution time in seconds
    """
    print("=== SEQUENTIAL EXECUTION ===\n")
    start_time = time.time()
    
    results = []
    for source, delay in sources:
        result = fetch_data(source, delay)
        results.append(result)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nSequential time: {total_time:.1f}s\n")
    return total_time


def run_threaded(sources):
    """
    Run all fetch operations using threading.
    
    Args:
        sources: List of tuples (source_name, delay)
        
    Returns:
        The total execution time in seconds
    """
    print("=== THREADED EXECUTION ===\n")
    start_time = time.time()
    
    # Use ThreadPoolExecutor to manage threads
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all tasks and get futures
        futures = [
            executor.submit(fetch_data, source, delay)
            for source, delay in sources
        ]
        
        # Wait for all tasks to complete
        results = [future.result() for future in futures]
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nThreaded time: {total_time:.1f}s\n")
    return total_time


def run_threading_manual(sources):
    """
    Run all fetch operations using manual Thread objects.
    
    Args:
        sources: List of tuples (source_name, delay)
        
    Returns:
        The total execution time in seconds
    """
    print("=== THREADING (MANUAL) EXECUTION ===\n")
    start_time = time.time()
    
    threads = []
    results = []
    
    # Create and start threads
    for source, delay in sources:
        thread = threading.Thread(
            target=lambda s=source, d=delay: fetch_data(s, d)
        )
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nThreading (manual) time: {total_time:.1f}s\n")
    return total_time


# Test code demonstrating threading benefits
if __name__ == "__main__":
    # Define the data sources with their simulated delays
    sources = [
        ("users", 2),
        ("orders", 3),
        ("products", 1),
        ("reviews", 2),
        ("inventory", 1)
    ]
    
    print("DATA SOURCES:")
    print("  users: 2s")
    print("  orders: 3s")
    print("  products: 1s")
    print("  reviews: 2s")
    print("  inventory: 1s")
    print("\nTheoretical times:")
    print("  Sequential: 2+3+1+2+1 = 9s")
    print("  Threaded: max(2,3,1,2,1) = 3s\n")
    print("=" * 50)
    print()
    
    # Run sequential execution
    seq_time = run_sequential(sources)
    
    # Add a small delay between runs
    time.sleep(0.5)
    
    # Run threaded execution using ThreadPoolExecutor
    thread_time = run_threaded(sources)
    
    # Add a small delay between runs
    time.sleep(0.5)
    
    # Run threaded execution using manual Thread objects
    manual_thread_time = run_threading_manual(sources)
    
    # Summary
    print("=" * 50)
    print("\n=== PERFORMANCE COMPARISON ===")
    print(f"Sequential time:        {seq_time:.1f}s")
    print(f"Threaded time (Pool):   {thread_time:.1f}s")
    print(f"Threaded time (Manual): {manual_thread_time:.1f}s")
    print(f"\nSpeedup (ThreadPoolExecutor): {seq_time/thread_time:.1f}x faster")
    print(f"Time saved: {seq_time - thread_time:.1f}s")
    
    print("\n=== KEY INSIGHTS ===")
    print("""
1. IO-bound operations benefit greatly from threading
2. ThreadPoolExecutor handles thread management automatically
3. Threading allows overlap of IO waits
4. Speedup ≈ number of parallel operations
5. Manual Thread objects provide more control but more code
    """)
