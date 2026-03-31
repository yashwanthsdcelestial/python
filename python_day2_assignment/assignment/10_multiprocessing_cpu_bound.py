import multiprocessing
import time


def compute_squares(n):
    """
    Compute the sum of squares from 1 to n.
    This is a CPU-bound operation using iteration for CPU intensity.
    
    Args:
        n: The upper limit
        
    Returns:
        The sum of squares
    """
    # Using iteration to create CPU-intensive work
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total


def run_sequential(values):
    """
    Run all computations sequentially.
    
    Args:
        values: List of integers to compute squares for
        
    Returns:
        Tuple of (results list, total execution time)
    """
    print("=== SEQUENTIAL EXECUTION ===\n")
    start_time = time.time()
    
    results = []
    for i, value in enumerate(values, 1):
        result = compute_squares(value)
        results.append(result)
        print(f"Task {i}: compute_squares({value:,}) = {result:,}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nSequential time: {total_time:.2f}s\n")
    return results, total_time


def run_multiprocessing(values):
    """
    Run all computations using multiprocessing.Pool.
    
    Args:
        values: List of integers to compute squares for
        
    Returns:
        Tuple of (results list, total execution time)
    """
    print("=== MULTIPROCESSING EXECUTION ===\n")
    start_time = time.time()
    
    # Get the number of CPU cores available
    num_processes = multiprocessing.cpu_count()
    print(f"CPU cores available: {num_processes}")
    print(f"Creating a pool with {num_processes} workers...\n")
    
    # Create a process pool and map the function
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(compute_squares, values)
    
    # Print results
    for i, (value, result) in enumerate(zip(values, results), 1):
        print(f"Task {i}: compute_squares({value:,}) = {result:,}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nMultiprocessing time: {total_time:.2f}s\n")
    return results, total_time


def run_multiprocessing_chunksize(values, chunksize=None):
    """
    Run all computations using multiprocessing.Pool with custom chunksize.
    
    Args:
        values: List of integers to compute squares for
        chunksize: The chunksize parameter for Pool.map()
        
    Returns:
        Tuple of (results list, total execution time)
    """
    print("=== MULTIPROCESSING EXECUTION (With Chunksize Optimization) ===\n")
    start_time = time.time()
    
    num_processes = multiprocessing.cpu_count()
    
    # Create a process pool and map the function with custom chunksize
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(compute_squares, values, chunksize=chunksize)
    
    # Print results
    for i, (value, result) in enumerate(zip(values, results), 1):
        print(f"Task {i}: compute_squares({value:,}) = {result:,}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nMultiprocessing (chunksize={chunksize}) time: {total_time:.2f}s\n")
    return results, total_time


# Test code demonstrating multiprocessing
if __name__ == "__main__":
    # Define the values - large enough for meaningful CPU-bound work
    # Note: With iterative approach, these numbers take noticeable time
    values = [30_000_000, 40_000_000, 35_000_000, 45_000_000]
    
    print("=" * 70)
    print("MULTIPROCESSING FOR CPU-BOUND OPERATIONS")
    print("=" * 70)
    print(f"\nComputing sum of squares for: {values}")
    print(f"Number of tasks: {len(values)}\n")
    
    # Run sequential execution
    seq_results, seq_time = run_sequential(values)
    
    # Add a small delay between runs
    time.sleep(0.5)
    
    # Run multiprocessing execution
    mp_results, mp_time = run_multiprocessing(values)
    
    # Add a small delay between runs
    time.sleep(0.5)
    
    # Run multiprocessing with optimized chunksize
    mp_chunk_results, mp_chunk_time = run_multiprocessing_chunksize(values, chunksize=1)
    
    # Verify all approaches produce the same results
    print("=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    print("\nVerifying all approaches produce identical results:")
    for i, (seq, mp, mp_chunk) in enumerate(zip(seq_results, mp_results, mp_chunk_results), 1):
        match = "✓" if seq == mp == mp_chunk else "✗"
        print(f"Task {i}: {match} Sequential={seq:,}, MP={mp:,}, MP_Chunk={mp_chunk:,}")
    
    # Performance comparison
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON")
    print("=" * 70)
    print(f"\nSequential execution time:              {seq_time:.2f}s")
    print(f"Multiprocessing time:                   {mp_time:.2f}s")
    print(f"Multiprocessing (chunked) time:         {mp_chunk_time:.2f}s")
    
    if mp_time < seq_time:
        speedup = seq_time / mp_time
        time_saved = seq_time - mp_time
        print(f"\nSpeedup (Multiprocessing):  {speedup:.2f}x faster")
        print(f"Time saved:                 {time_saved:.2f}s")
    
    print("\n" + "=" * 70)
    print("WHY MULTIPROCESSING WORKS FOR CPU-BOUND OPERATIONS")
    print("=" * 70)
    print("""
THREADING vs MULTIPROCESSING:

Threading:
  • Limited by Python's Global Interpreter Lock (GIL)
  • GIL allows only ONE thread to execute Python bytecode at a time
  • Good for IO-bound operations (waiting doesn't hold GIL)
  • Poor for CPU-bound operations (still sequential due to GIL)

Multiprocessing:
  • Each process has its own Python interpreter and GIL
  • Processes can run in parallel on different CPU cores
  • Perfect for CPU-bound operations
  • Overhead: Inter-process communication is slower than threading

CPU-BOUND EXAMPLE:
  • CPU-intensive calculations (like computing squares)
  • Data processing and scientific computing
  • Image/video processing
  • Machine learning model training

MULTIPROCESSING MODEL:
  Sequential:     [Task1] [Task2] [Task3] [Task4]  →  Total: T1+T2+T3+T4
  Multiprocessing: [Task1] →
                   [Task2] →  (Running in parallel on different cores)
                   [Task3] →
                   [Task4] →  Total: max(T1, T2, T3, T4)

POOL.MAP() Benefits:
  • Automatically distributes tasks to worker processes
  • Handles process creation/termination
  • Simple interface: pool.map(function, iterable)
  • Maintains order of results
    """)
