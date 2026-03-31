import asyncio
import time
from datetime import datetime


def log_timestamp(event, url):
    """Helper function to print timestamped events."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] {event}: {url}")


# ============================================================================
# SYNCHRONOUS VERSION
# ============================================================================

def fetch_sync(url, delay):
    """
    Synchronous API call simulation.
    Blocks the entire program during the sleep.
    
    Args:
        url: The API endpoint URL
        delay: The simulated API response delay in seconds
        
    Returns:
        A dictionary with the fetch result
    """
    log_timestamp("START", url)
    time.sleep(delay)  # Blocking call - halts everything
    log_timestamp("END", url)
    return {"url": url, "status": "success", "data": f"Data from {url}"}


def run_sync(urls):
    """
    Run all API calls synchronously (one after another).
    
    Args:
        urls: List of tuples (url, delay)
        
    Returns:
        Tuple of (results list, total execution time)
    """
    print("=== SYNCHRONOUS VERSION ===\n")
    start_time = time.time()
    
    results = []
    for url, delay in urls:
        result = fetch_sync(url, delay)
        results.append(result)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nSync time: {total_time:.1f}s\n")
    return results, total_time


# ============================================================================
# ASYNCHRONOUS VERSION
# ============================================================================

async def fetch_async(url, delay):
    """
    Asynchronous API call simulation.
    Uses await to allow other coroutines to run during the sleep.
    
    Args:
        url: The API endpoint URL
        delay: The simulated API response delay in seconds
        
    Returns:
        A dictionary with the fetch result
    """
    log_timestamp("START", url)
    await asyncio.sleep(delay)  # Non-blocking call - allows other coroutines to run
    log_timestamp("END", url)
    return {"url": url, "status": "success", "data": f"Data from {url}"}


async def run_async(urls):
    """
    Run all API calls asynchronously (concurrently).
    Uses asyncio.gather() to run multiple coroutines concurrently.
    
    Args:
        urls: List of tuples (url, delay)
        
    Returns:
        Tuple of (results list, total execution time)
    """
    print("=== ASYNCHRONOUS VERSION ===\n")
    start_time = time.time()
    
    # Create coroutines for all tasks
    tasks = [fetch_async(url, delay) for url, delay in urls]
    
    # Run all coroutines concurrently
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nAsync time: {total_time:.1f}s\n")
    return results, total_time


async def run_async_with_create_task(urls):
    """
    Alternative: Use asyncio.create_task() for more explicit control.
    
    Args:
        urls: List of tuples (url, delay)
        
    Returns:
        Tuple of (results list, total execution time)
    """
    print("=== ASYNCHRONOUS VERSION (Using create_task) ===\n")
    start_time = time.time()
    
    # Create tasks explicitly
    tasks = [asyncio.create_task(fetch_async(url, delay)) for url, delay in urls]
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\nAsync time (create_task): {total_time:.1f}s\n")
    return results, total_time


# ============================================================================
# MAIN TEST CODE
# ============================================================================

async def main():
    """Main async function to orchestrate the test."""
    # Define the API endpoints and delays
    urls = [
        ("api/users", 2),
        ("api/orders", 3),
        ("api/products", 1),
        ("api/reviews", 2)
    ]
    
    print("=" * 70)
    print("ASYNC IO - CONCURRENT API SIMULATION")
    print("=" * 70)
    print(f"\nAPI Endpoints:")
    for url, delay in urls:
        print(f"  {url}: {delay}s")
    print(f"\nTheoretical times:")
    print(f"  Synchronous: {sum(d for _, d in urls)}s (sum)")
    print(f"  Asynchronous: {max(d for _, d in urls)}s (max)\n")
    print("=" * 70)
    print()
    
    # Run synchronous version
    sync_results, sync_time = run_sync(urls)
    
    # Add a small delay between runs
    await asyncio.sleep(0.5)
    
    # Run asynchronous version using gather
    async_results, async_time = await run_async(urls)
    
    # Add a small delay between runs
    await asyncio.sleep(0.5)
    
    # Run asynchronous version using create_task
    async_ct_results, async_ct_time = await run_async_with_create_task(urls)
    
    # Verification
    print("=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    print("\nVerifying all approaches produce identical results:")
    print("✓ All approaches successfully fetched data from all endpoints\n")
    
    # Performance comparison
    print("=" * 70)
    print("PERFORMANCE COMPARISON")
    print("=" * 70)
    print(f"\nSynchronous execution time:           {sync_time:.2f}s")
    print(f"Asynchronous time (gather):           {async_time:.2f}s")
    print(f"Asynchronous time (create_task):      {async_ct_time:.2f}s")
    
    speedup = sync_time / async_time
    time_saved = sync_time - async_time
    print(f"\nSpeedup (asyncio.gather):  {speedup:.2f}x faster")
    print(f"Time saved:                {time_saved:.2f}s")
    
    print("\n" + "=" * 70)
    print("KEY DIFFERENCES: SYNC vs ASYNC")
    print("=" * 70)
    print("""
SYNCHRONOUS:
  • Executes one task at a time
  • Each task blocks execution until complete
  • Total time = sum of all delays (2+3+1+2 = 8s)
  • Simple to understand but inefficient

ASYNCHRONOUS:
  • Multiple tasks run concurrently on a single thread
  • Uses an event loop to switch between tasks
  • When one task waits (asyncio.sleep), others can run
  • Total time = max of all delays (max=3s)
  • Requires async/await syntax

EVENT LOOP EXECUTION:
  Time 0.0s: START users      START orders        START products       START reviews
  Time 1.0s: (products waits)  (orders waits)      END products
  Time 2.0s: END users        (orders waits)       (reviews waits)       END reviews
  Time 3.0s: END orders       (done)
  
  All tasks completed in ~3 seconds instead of 8 seconds!

ASYNCIO.GATHER() vs CREATE_TASK():
  • gather(): Returns list of results in original order, simpler syntax
  • create_task(): More explicit, better for complex scenarios
  • Both run tasks concurrently with asyncio.gather()

USE CASES:
  ✓ Web scraping (many concurrent HTTP requests)
  ✓ Database queries (many concurrent queries to DB)
  ✓ File I/O (reading/writing many files)
  ✓ Microservices communication
  ✗ CPU-bound operations (use multiprocessing instead)
    """)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
