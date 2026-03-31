"""
Q20: Map HTTP Status Codes to Categories

Problem: Classify HTTP response codes into categories using list comprehension.

Topics: List Comprehension, HTTP Status Codes, Conditional Logic

Constraints:
- 2xx → success, 3xx → redirect, 4xx → client_error, 5xx → server_error
- Use a single list comprehension with a helper function or inline conditional
"""

# ============================================================================
# SOLUTION - Main Approach (With Helper Function)
# ============================================================================

def categorize_http_code(code):
    """Helper function to categorize a single HTTP code"""
    if 200 <= code < 300:
        return 'success'
    elif 300 <= code < 400:
        return 'redirect'
    elif 400 <= code < 500:
        return 'client_error'
    elif 500 <= code < 600:
        return 'server_error'
    else:
        return 'unknown'


def map_http_codes_to_categories(codes):
    """
    Classify HTTP codes using list comprehension with helper function.
    
    Args:
        codes: List of HTTP response codes (integers)
        
    Returns:
        List of tuples (code, category)
    """
    return [(code, categorize_http_code(code)) for code in codes]


# ============================================================================
# ALTERNATIVE APPROACHES
# ============================================================================

def map_http_codes_inline(codes):
    """
    Classify HTTP codes using inline conditional (ternary chain).
    Single line comprehension with nested conditionals.
    """
    return [(code, 'success' if 200 <= code < 300 
                       else 'redirect' if 300 <= code < 400
                       else 'client_error' if 400 <= code < 500
                       else 'server_error' if 500 <= code < 600
                       else 'unknown') for code in codes]


def map_http_codes_with_dict(codes):
    """
    Using dictionary lookup with range-based categorization.
    More functional approach.
    """
    categories = {
        2: 'success',
        3: 'redirect',
        4: 'client_error',
        5: 'server_error',
    }
    return [(code, categories.get(code // 100, 'unknown')) for code in codes]


def map_http_codes_with_ranges(codes):
    """
    Using range objects for category mapping.
    """
    category_ranges = [
        (range(200, 300), 'success'),
        (range(300, 400), 'redirect'),
        (range(400, 500), 'client_error'),
        (range(500, 600), 'server_error'),
    ]
    
    def get_category(code):
        for r, category in category_ranges:
            if code in r:
                return category
        return 'unknown'
    
    return [(code, get_category(code)) for code in codes]


# ============================================================================
# TEST DATA
# ============================================================================

codes_main = [200, 201, 404, 500, 301, 403, 502, 204]

expected_main = [
    (200, 'success'),
    (201, 'success'),
    (404, 'client_error'),
    (500, 'server_error'),
    (301, 'redirect'),
    (403, 'client_error'),
    (502, 'server_error'),
    (204, 'success')
]


# ============================================================================
# TESTS
# ============================================================================

def test_main_solution():
    """Test the main solution with provided example"""
    result = map_http_codes_to_categories(codes_main)
    assert result == expected_main, f"Expected {expected_main}, got {result}"
    print("✅ Main solution test passed")
    print(f"   Input: {codes_main}")
    print(f"   Output: {result}")


def test_empty_codes():
    """Test with empty code list"""
    result = map_http_codes_to_categories([])
    assert result == [], f"Expected [], got {result}"
    print("✅ Empty codes test passed")


def test_all_success_codes():
    """Test with only success codes"""
    codes = [200, 201, 202, 204, 206]
    result = map_http_codes_to_categories(codes)
    expected = [(code, 'success') for code in codes]
    assert result == expected, f"Got {result}"
    print("✅ All success codes test passed")


def test_all_redirect_codes():
    """Test with only redirect codes"""
    codes = [300, 301, 302, 304, 307, 308]
    result = map_http_codes_to_categories(codes)
    expected = [(code, 'redirect') for code in codes]
    assert result == expected, f"Got {result}"
    print("✅ All redirect codes test passed")


def test_all_client_error_codes():
    """Test with only client error codes"""
    codes = [400, 401, 403, 404, 405, 408, 429, 499]
    result = map_http_codes_to_categories(codes)
    expected = [(code, 'client_error') for code in codes]
    assert result == expected, f"Got {result}"
    print("✅ All client error codes test passed")


def test_all_server_error_codes():
    """Test with only server error codes"""
    codes = [500, 501, 502, 503, 504, 599]
    result = map_http_codes_to_categories(codes)
    expected = [(code, 'server_error') for code in codes]
    assert result == expected, f"Got {result}"
    print("✅ All server error codes test passed")


def test_boundary_values():
    """Test boundary values for each category"""
    codes = [199, 200, 299, 300, 399, 400, 499, 500, 599, 600]
    result = map_http_codes_to_categories(codes)
    expected = [
        (199, 'unknown'),
        (200, 'success'),
        (299, 'success'),
        (300, 'redirect'),
        (399, 'redirect'),
        (400, 'client_error'),
        (499, 'client_error'),
        (500, 'server_error'),
        (599, 'server_error'),
        (600, 'unknown'),
    ]
    assert result == expected, f"Got {result}"
    print("✅ Boundary values test passed")


def test_single_code():
    """Test with single code"""
    result = map_http_codes_to_categories([404])
    assert result == [(404, 'client_error')], f"Got {result}"
    print("✅ Single code test passed")


def test_common_codes():
    """Test with most common HTTP codes"""
    codes = [
        200,  # OK
        201,  # Created
        204,  # No Content
        301,  # Moved Permanently
        302,  # Found
        304,  # Not Modified
        400,  # Bad Request
        401,  # Unauthorized
        403,  # Forbidden
        404,  # Not Found
        500,  # Internal Server Error
        502,  # Bad Gateway
        503,  # Service Unavailable
    ]
    result = map_http_codes_to_categories(codes)
    
    # Verify all codes are present and correctly categorized
    assert len(result) == len(codes), "Result length mismatch"
    
    # Check specific codes
    assert result[0] == (200, 'success')
    assert result[3] == (301, 'redirect')
    assert result[7] == (401, 'client_error')
    assert result[10] == (500, 'server_error')
    
    print("✅ Common codes test passed")


def test_unusual_codes():
    """Test with non-standard codes"""
    codes = [100, 418, 599, 999, -1, 0]
    result = map_http_codes_to_categories(codes)
    
    # These should map appropriately or to 'unknown'
    expected = [
        (100, 'unknown'),     # 1xx not in our categories
        (418, 'client_error'), # I'm a teapot
        (599, 'server_error'), # Server error
        (999, 'unknown'),      # Out of range
        (-1, 'unknown'),       # Negative
        (0, 'unknown'),        # Zero
    ]
    assert result == expected, f"Got {result}"
    print("✅ Unusual codes test passed")


def test_alternatives_equivalence():
    """Test that all approaches produce same results"""
    result1 = map_http_codes_to_categories(codes_main)
    result2 = map_http_codes_inline(codes_main)
    result3 = map_http_codes_with_dict(codes_main)
    result4 = map_http_codes_with_ranges(codes_main)
    
    assert result1 == result2 == result3 == result4, "All approaches should match"
    print("✅ Alternatives equivalence test passed")
    print(f"   Helper function: {result1}")
    print(f"   Inline ternary:  {result2}")
    print(f"   Dict lookup:     {result3}")
    print(f"   Range matching:  {result4}")


def test_large_dataset():
    """Test with large dataset"""
    # Generate a variety of codes
    codes = list(range(100, 600, 7))  # ~71 codes across all ranges
    result = map_http_codes_to_categories(codes)
    
    # Verify structure
    assert len(result) == len(codes), "Should have one result per code"
    
    # Verify all are tuples
    assert all(isinstance(r, tuple) and len(r) == 2 for r in result), "All should be 2-tuples"
    
    # Verify all have valid categories
    valid_categories = {'success', 'redirect', 'client_error', 'server_error', 'unknown'}
    assert all(r[1] in valid_categories for r in result), "Invalid categories found"
    
    print(f"✅ Large dataset test passed ({len(result)} codes)")


# ============================================================================
# COMPREHENSION BREAKDOWN
# ============================================================================

def analyze_comprehension():
    """Detailed breakdown of the comprehension syntax"""
    codes = codes_main
    
    print("\n" + "="*70)
    print("COMPREHENSION BREAKDOWN: [(code, categorize_http_code(code)) for code in codes]")
    print("="*70)
    
    print("\nSyntax Structure:")
    print("  [(code, categorize_http_code(code)) for code in codes]")
    print("  └─ List Comprehension (creates list of tuples)")
    print("     ├─ (code, categorize_http_code(code)): Tuple expression")
    print("     │  ├─ code: The HTTP code itself")
    print("     │  └─ categorize_http_code(code): Category from helper function")
    print("     └─ for code in codes: Iterate through each code")
    
    print("\nExecution Flow:")
    for i, code in enumerate(codes, 1):
        category = categorize_http_code(code)
        print(f"  {i}. Code {code} → Category '{category}'")
    
    print("\nHelper Function Logic:")
    print("""
    def categorize_http_code(code):
        if 200 <= code < 300:
            return 'success'
        elif 300 <= code < 400:
            return 'redirect'
        elif 400 <= code < 500:
            return 'client_error'
        elif 500 <= code < 600:
            return 'server_error'
        else:
            return 'unknown'
    
    This separates the categorization logic from the comprehension.
    Makes the comprehension more readable and the helper reusable.
    """)


# ============================================================================
# INLINE CONDITIONAL APPROACH
# ============================================================================

def analyze_inline_approach():
    """Explanation of the inline conditional approach"""
    print("\n" + "="*70)
    print("INLINE CONDITIONAL APPROACH (Nested Ternary)")
    print("="*70)
    
    print("""
    return [(code, 'success' if 200 <= code < 300 
                          else 'redirect' if 300 <= code < 400
                          else 'client_error' if 400 <= code < 500
                          else 'server_error' if 500 <= code < 600
                          else 'unknown') for code in codes]
    
    This puts all logic inline without a helper function.
    
    Advantages:
      • Single line comprehension (all logic self-contained)
      • No need for separate function definition
      • Can be more readable with proper formatting
    
    Disadvantages:
      • Harder to test the categorization logic separately
      • Long and nested conditionals
      • Less reusable if need to categorize codes elsewhere
    
    The nested ternary works as:
      'success' if 200 <= code < 300 else ...
         └─ Returns 'success' for 2xx codes
            else (if previous condition false) → evaluate next condition
    """)


# ============================================================================
# DICT LOOKUP APPROACH
# ============================================================================

def analyze_dict_approach():
    """Explanation of the dictionary lookup approach"""
    print("\n" + "="*70)
    print("DICTIONARY LOOKUP APPROACH")
    print("="*70)
    
    print("""
    categories = {2: 'success', 3: 'redirect', 4: 'client_error', 5: 'server_error'}
    return [(code, categories.get(code // 100, 'unknown')) for code in codes]
    
    This uses integer division to extract the first digit of the code.
    
    How it works:
      • code // 100 extracts the first digit
      • 200 // 100 = 2 (success)
      • 404 // 404 = 4 (client_error)
      • 500 // 100 = 5 (server_error)
      • categories.get(key, default) provides fallback for unknown codes
    
    Advantages:
      • Very concise and elegant
      • O(1) lookup time
      • Easy to extend with more categories
      • Most Pythonic approach
      
    Disadvantages:
      • Magic number (100) might not be immediately obvious
      • Less explicit about range boundaries
      • Less readable for those unfamiliar with the HTTP code structure
    """)


# ============================================================================
# REAL-WORLD EXAMPLES
# ============================================================================

def example_api_response_logging():
    """Real-world: Log API responses by category"""
    api_responses = [200, 200, 201, 404, 500, 200, 502, 404]
    responses = map_http_codes_to_categories(api_responses)
    
    # Count by category
    by_category = {}
    for code, category in responses:
        by_category.setdefault(category, []).append(code)
    
    print(f"\nAPI Response Logging Example:")
    print(f"  Total responses: {len(responses)}")
    for category in sorted(by_category.keys()):
        codes = by_category[category]
        print(f"  {category}: {len(codes)} responses → {codes}")


def example_web_scraper():
    """Real-world: Handle different HTTP response codes in web scraper"""
    status_codes = [200, 200, 301, 200, 404, 403, 500, 200, 301, 502]
    categorized = map_http_codes_to_categories(status_codes)
    
    print(f"\nWeb Scraper Example:")
    print(f"  URLs crawled: {len(status_codes)}")
    
    actions = {
        'success': 'Process page content',
        'redirect': 'Follow redirect',
        'client_error': 'Log error, skip page',
        'server_error': 'Retry later',
        'unknown': 'Unknown status'
    }
    
    for code, category in categorized:
        print(f"  Code {code} ({category}): {actions.get(category, '?')}")


def example_monitoring_dashboard():
    """Real-world: Monitor HTTP status codes on a dashboard"""
    hourly_codes = [
        200, 200, 200, 201, 200, 404, 200, 500, 200, 200,  # Hour 1
        200, 200, 502, 200, 200, 301, 200, 200, 200, 200,  # Hour 2
    ]
    categorized = map_http_codes_to_categories(hourly_codes)
    
    # Summary statistics
    stats = {}
    for code, category in categorized:
        stats.setdefault(category, 0)
        stats[category] += 1
    
    total = len(categorized)
    print(f"\nMonitoring Dashboard Example (20 requests):")
    for category in sorted(stats.keys()):
        count = stats[category]
        percentage = (count / total) * 100
        print(f"  {category}: {count} ({percentage:.1f}%)")


def example_http_client_library():
    """Real-world: HTTP client decides what to do with each response"""
    responses = [200, 404, 500, 301, 403]
    categorized = map_http_codes_to_categories(responses)
    
    print(f"\nHTTP Client Library Example:")
    for code, category in categorized:
        if category == 'success':
            action = "✓ Return response to caller"
        elif category == 'redirect':
            action = "→ Follow redirect"
        elif category == 'client_error':
            action = "✗ Return error details"
        elif category == 'server_error':
            action = "↻ Retry with backoff"
        else:
            action = "? Unknown handling"
        print(f"  {code}: {action}")


# ============================================================================
# PERFORMANCE ANALYSIS
# ============================================================================

def performance_comparison():
    """Compare performance of different approaches"""
    import time
    
    # Create larger dataset
    codes = list(range(100, 600)) * 10  # 5000 codes
    
    print("\n" + "="*70)
    print("PERFORMANCE COMPARISON (5000 codes)")
    print("="*70)
    
    # Approach 1: Helper function
    start = time.time()
    for _ in range(100):
        result1 = map_http_codes_to_categories(codes)
    time1 = time.time() - start
    print(f"\nHelper function approach: {time1:.6f}s (for 100 iterations)")
    
    # Approach 2: Inline conditional
    start = time.time()
    for _ in range(100):
        result2 = map_http_codes_inline(codes)
    time2 = time.time() - start
    print(f"Inline conditional approach: {time2:.6f}s")
    
    # Approach 3: Dictionary lookup
    start = time.time()
    for _ in range(100):
        result3 = map_http_codes_with_dict(codes)
    time3 = time.time() - start
    print(f"Dictionary lookup approach: {time3:.6f}s")
    
    # Approach 4: Range matching
    start = time.time()
    for _ in range(100):
        result4 = map_http_codes_with_ranges(codes)
    time4 = time.time() - start
    print(f"Range matching approach: {time4:.6f}s")
    
    fastest = min(time1, time2, time3, time4)
    print(f"\n✓ Helper function: {(time1/fastest*100):.1f}%")
    print(f"✓ Inline conditional: {(time2/fastest*100):.1f}%")
    print(f"✓ Dictionary lookup: {(time3/fastest*100):.1f}% (FASTEST)")
    print(f"✓ Range matching: {(time4/fastest*100):.1f}%")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("Q20: MAP HTTP STATUS CODES TO CATEGORIES")
    print("="*70)
    
    # Run all tests
    print("\n" + "="*70)
    print("RUNNING TESTS")
    print("="*70)
    test_main_solution()
    test_empty_codes()
    test_all_success_codes()
    test_all_redirect_codes()
    test_all_client_error_codes()
    test_all_server_error_codes()
    test_boundary_values()
    test_single_code()
    test_common_codes()
    test_unusual_codes()
    test_alternatives_equivalence()
    test_large_dataset()
    
    # Analysis
    analyze_comprehension()
    analyze_inline_approach()
    analyze_dict_approach()
    
    # Real-world examples
    print("\n" + "="*70)
    print("REAL-WORLD EXAMPLES")
    print("="*70)
    example_api_response_logging()
    example_web_scraper()
    example_monitoring_dashboard()
    example_http_client_library()
    
    # Performance
    performance_comparison()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
