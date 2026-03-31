"""
Q19: Flatten and Deduplicate Tags

Problem: Extract all unique tags from articles, sorted alphabetically.

Topics: List Comprehension, Sets, Nested Iteration

Constraints:
- Use set comprehension or list comprehension with set conversion
- Output must be sorted alphabetically
- Solve in no more than 2 lines of code
"""

# ============================================================================
# SOLUTION
# ============================================================================

def flatten_and_deduplicate_tags(articles):
    """
    Extract all unique tags from articles and sort alphabetically.
    
    Args:
        articles: List of dicts with "tags" key containing tag lists
        
    Returns:
        Sorted list of unique tags
    """
    # Solution (1 line with set comprehension + sorted)
    return sorted({tag for article in articles for tag in article["tags"]})


# Alternative 1-liner (2 lines if assigned to variable)
def flatten_and_deduplicate_tags_alt1(articles):
    """Using list comprehension with set conversion"""
    unique_tags = {tag for article in articles for tag in article["tags"]}
    return sorted(unique_tags)


# Alternative using nested list comprehension + set conversion
def flatten_and_deduplicate_tags_alt2(articles):
    """Using nested list comprehension"""
    return sorted(set(tag for article in articles for tag in article["tags"]))


# ============================================================================
# TEST DATA
# ============================================================================

articles_main = [
    {"title": "AI Intro", "tags": ["python", "ml", "ai"]},
    {"title": "Web Dev", "tags": ["python", "fastapi", "api"]},
    {"title": "Data 101", "tags": ["ml", "pandas", "python"]},
]

expected_main = ['ai', 'api', 'fastapi', 'ml', 'pandas', 'python']


# ============================================================================
# TESTS
# ============================================================================

def test_main_solution():
    """Test the main solution with provided example"""
    result = flatten_and_deduplicate_tags(articles_main)
    assert result == expected_main, f"Expected {expected_main}, got {result}"
    print("✅ Main solution test passed")
    print(f"   Input: {len(articles_main)} articles")
    print(f"   Output: {result}")


def test_empty_articles():
    """Test with empty articles list"""
    result = flatten_and_deduplicate_tags([])
    assert result == [], f"Expected [], got {result}"
    print("✅ Empty articles test passed")


def test_single_article():
    """Test with single article"""
    articles = [{"title": "Single", "tags": ["python", "coding"]}]
    result = flatten_and_deduplicate_tags(articles)
    assert result == ['coding', 'python'], f"Got {result}"
    print("✅ Single article test passed")


def test_duplicate_tags_heavy():
    """Test with lots of duplicate tags"""
    articles = [
        {"title": "A", "tags": ["python", "python", "ai", "ai"]},
        {"title": "B", "tags": ["python", "ai", "ml"]},
    ]
    result = flatten_and_deduplicate_tags(articles)
    # Set automatically deduplicates, so duplicates within articles are removed
    assert result == ['ai', 'ml', 'python'], f"Got {result}"
    print("✅ Heavy duplicate tags test passed")


def test_empty_tags():
    """Test with articles having empty tag lists"""
    articles = [
        {"title": "A", "tags": []},
        {"title": "B", "tags": ["python"]},
        {"title": "C", "tags": []},
    ]
    result = flatten_and_deduplicate_tags(articles)
    assert result == ['python'], f"Got {result}"
    print("✅ Empty tags test passed")


def test_single_tag_per_article():
    """Test where each article has only one tag"""
    articles = [
        {"title": "A", "tags": ["python"]},
        {"title": "B", "tags": ["java"]},
        {"title": "C", "tags": ["rust"]},
    ]
    result = flatten_and_deduplicate_tags(articles)
    assert result == ['java', 'python', 'rust'], f"Got {result}"
    print("✅ Single tag per article test passed")


def test_case_sensitivity():
    """Test that tags are case-sensitive"""
    articles = [
        {"title": "A", "tags": ["Python", "python"]},
        {"title": "B", "tags": ["PYTHON"]},
    ]
    result = flatten_and_deduplicate_tags(articles)
    # All different cases are preserved and sorted
    assert result == ['PYTHON', 'Python', 'python'], f"Got {result}"
    print("✅ Case sensitivity test passed")


def test_special_characters_and_numbers():
    """Test tags with special characters and numbers"""
    articles = [
        {"title": "A", "tags": ["web3.0", "ai-ml", "c++"]},
        {"title": "B", "tags": ["node.js", "ai-ml", "web3.0"]},
    ]
    result = flatten_and_deduplicate_tags(articles)
    # Alphabetical sort respects special characters
    assert result == sorted(['web3.0', 'ai-ml', 'c++', 'node.js']), f"Got {result}"
    print("✅ Special characters and numbers test passed")


def test_large_dataset():
    """Test with many articles and tags"""
    articles = [
        {"title": f"Article {i}", "tags": [f"tag{j}" for j in range((i % 10) + 1)]}
        for i in range(100)
    ]
    result = flatten_and_deduplicate_tags(articles)
    # Should have unique tags from tag0 to tag9
    expected = sorted([f"tag{i}" for i in range(10)])
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✅ Large dataset test passed ({len(articles)} articles, {len(result)} unique tags)")


def test_alternatives_equivalence():
    """Test that all approaches produce the same result"""
    result1 = flatten_and_deduplicate_tags(articles_main)
    result2 = flatten_and_deduplicate_tags_alt1(articles_main)
    result3 = flatten_and_deduplicate_tags_alt2(articles_main)
    
    assert result1 == result2 == result3, "All approaches should produce same result"
    print("✅ Alternatives equivalence test passed")
    print(f"   All 3 approaches produce: {result1}")


# ============================================================================
# COMPREHENSION BREAKDOWN
# ============================================================================

def analyze_comprehension():
    """Detailed breakdown of the comprehension syntax"""
    articles = articles_main
    
    print("\n" + "="*70)
    print("COMPREHENSION BREAKDOWN: {tag for article in articles for tag in article['tags']}")
    print("="*70)
    
    print("\nSyntax Structure:")
    print("  {tag for article in articles for tag in article['tags']}")
    print("  └─ Set Comprehension (will deduplicate)")
    print("     ├─ tag: Expression being collected (the item to add to set)")
    print("     ├─ for article in articles: Outer loop (iterate through each article)")
    print("     └─ for tag in article['tags']: Inner loop (iterate through article's tags)")
    
    print("\nExecution Flow:")
    for i, article in enumerate(articles, 1):
        print(f"  {i}. Article: {article['title']}")
        print(f"     Tags: {article['tags']}")
        for tag in article['tags']:
            print(f"     → Add '{tag}' to set")
    
    print("\nSet Collection Process:")
    tags_set = {tag for article in articles for tag in article["tags"]}
    print(f"  Collected tags (unordered set): {tags_set}")
    
    print("\nAfter Sorting:")
    sorted_tags = sorted(tags_set)
    print(f"  Sorted tags: {sorted_tags}")
    
    print("\nDeduplication Details:")
    print(f"  Total tag occurrences: {sum(len(a['tags']) for a in articles)}")
    print(f"  Unique tags (after set): {len(tags_set)}")
    print(f"  Duplicates removed: {sum(len(a['tags']) for a in articles) - len(tags_set)}")


# ============================================================================
# ALTERNATIVE APPROACHES
# ============================================================================

def approach_with_dict():
    """Using dict.fromkeys() to preserve order in Python 3.7+"""
    articles = articles_main
    # Flatten all tags, then use dict.fromkeys for deduplication
    all_tags = [tag for article in articles for tag in article["tags"]]
    return sorted(dict.fromkeys(all_tags))


def approach_with_loop_and_set():
    """Traditional approach with explicit loop"""
    articles = articles_main
    tags = set()
    for article in articles:
        for tag in article["tags"]:
            tags.add(tag)
    return sorted(tags)


def approach_with_chain():
    """Using itertools.chain (requires import)"""
    from itertools import chain
    articles = articles_main
    all_tags = chain.from_iterable(article["tags"] for article in articles)
    return sorted(set(all_tags))


def test_alternative_approaches():
    """Verify alternative approaches work"""
    main_result = flatten_and_deduplicate_tags(articles_main)
    
    print("\n" + "="*70)
    print("ALTERNATIVE APPROACHES")
    print("="*70)
    
    result_dict = approach_with_dict()
    result_loop = approach_with_loop_and_set()
    result_chain = approach_with_chain()
    
    print(f"\n✓ dict.fromkeys() approach: {result_dict}")
    assert result_dict == main_result
    
    print(f"✓ Loop + set approach: {result_loop}")
    assert result_loop == main_result
    
    print(f"✓ itertools.chain() approach: {result_chain}")
    assert result_chain == main_result
    
    print("\n✅ All alternative approaches produce identical results")


# ============================================================================
# REAL-WORLD EXAMPLES
# ============================================================================

def example_blog_categories():
    """Real-world: Extract all blog categories"""
    blog_posts = [
        {"url": "/post-1", "categories": ["tech", "python", "tutorial"]},
        {"url": "/post-2", "categories": ["python", "databases", "tutorial"]},
        {"url": "/post-3", "categories": ["web", "fastapi", "api"]},
        {"url": "/post-4", "categories": ["tech", "databases"]},
    ]
    unique_categories = sorted({cat for post in blog_posts for cat in post["categories"]})
    print(f"\nBlog Categories Example:")
    print(f"  Blog posts: {len(blog_posts)}")
    print(f"  Unique categories: {unique_categories}")
    return unique_categories


def example_movie_genres():
    """Real-world: Extract all movie genres from watch history"""
    watch_history = [
        {"title": "Movie A", "genres": ["action", "sci-fi", "thriller"]},
        {"title": "Movie B", "genres": ["comedy", "romance"]},
        {"title": "Movie C", "genres": ["drama", "sci-fi"]},
        {"title": "Movie D", "genres": ["action", "comedy"]},
    ]
    all_genres = sorted({genre for movie in watch_history for genre in movie["genres"]})
    print(f"\nMovie Genres Example:")
    print(f"  Movies watched: {len(watch_history)}")
    print(f"  All genres: {all_genres}")
    return all_genres


def example_product_tags():
    """Real-world: Extract all product tags for e-commerce search"""
    products = [
        {"id": 1, "name": "Laptop", "tags": ["electronics", "computers", "expensive"]},
        {"id": 2, "name": "Mouse", "tags": ["electronics", "accessories", "cheap"]},
        {"id": 3, "name": "Monitor", "tags": ["electronics", "expensive", "displays"]},
        {"id": 4, "name": "Keyboard", "tags": ["accessories", "cheap", "input"]},
    ]
    searchable_tags = sorted({tag for product in products for tag in product["tags"]})
    print(f"\nE-commerce Tags Example:")
    print(f"  Products: {len(products)}")
    print(f"  Searchable tags: {searchable_tags}")
    return searchable_tags


# ============================================================================
# PERFORMANCE ANALYSIS
# ============================================================================

def performance_comparison():
    """Compare performance of different approaches"""
    import time
    
    # Create larger dataset
    articles = [
        {"title": f"Article {i}", "tags": [f"tag{j}" for j in range(5)]}
        for i in range(1000)
    ]
    
    print("\n" + "="*70)
    print("PERFORMANCE COMPARISON (1000 articles, 5 tags each)")
    print("="*70)
    
    # Approach 1: Set comprehension + sorted
    start = time.time()
    for _ in range(100):
        result1 = sorted({tag for article in articles for tag in article["tags"]})
    time1 = time.time() - start
    print(f"\nSet comprehension + sorted: {time1:.6f}s (for 100 iterations)")
    
    # Approach 2: List comprehension + set + sorted
    start = time.time()
    for _ in range(100):
        result2 = sorted(set(tag for article in articles for tag in article["tags"]))
    time2 = time.time() - start
    print(f"List comprehension + set + sorted: {time2:.6f}s")
    
    # Approach 3: Loop + set
    start = time.time()
    for _ in range(100):
        tags = set()
        for article in articles:
            for tag in article["tags"]:
                tags.add(tag)
        result3 = sorted(tags)
    time3 = time.time() - start
    print(f"Loop + set (traditional): {time3:.6f}s")
    
    # Approach 4: itertools.chain
    from itertools import chain
    start = time.time()
    for _ in range(100):
        result4 = sorted(set(chain.from_iterable(a["tags"] for a in articles)))
    time4 = time.time() - start
    print(f"itertools.chain + set: {time4:.6f}s")
    
    print(f"\n✓ Sets comprehension: 100% (fastest)")
    print(f"✓ List comprehension + set: {(time2/time1*100):.1f}%")
    print(f"✓ Traditional loop: {(time3/time1*100):.1f}%")
    print(f"✓ itertools.chain: {(time4/time1*100):.1f}%")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("Q19: FLATTEN AND DEDUPLICATE TAGS")
    print("="*70)
    
    # Run all tests
    print("\n" + "="*70)
    print("RUNNING TESTS")
    print("="*70)
    test_main_solution()
    test_empty_articles()
    test_single_article()
    test_duplicate_tags_heavy()
    test_empty_tags()
    test_single_tag_per_article()
    test_case_sensitivity()
    test_special_characters_and_numbers()
    test_large_dataset()
    test_alternatives_equivalence()
    
    # Analysis and comparisons
    analyze_comprehension()
    test_alternative_approaches()
    
    # Real-world examples
    print("\n" + "="*70)
    print("REAL-WORLD EXAMPLES")
    print("="*70)
    example_blog_categories()
    example_movie_genres()
    example_product_tags()
    
    # Performance
    performance_comparison()
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
