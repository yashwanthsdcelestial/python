"""
Q18 - Filter and Transform with Dictionary Comprehension

Topics: Dictionary Comprehension

Problem Statement:
Given a list of user dictionaries, use a single dictionary comprehension
to create a mapping of username → email for users who are active and aged 18+.

Input: List of user dictionaries with username, email, age, and active status
Output: Dictionary mapping username to email for eligible users

Constraints:
- Use a single dictionary comprehension (one line)
- Both conditions (active AND age >= 18) must be met
"""


# ============================================================================
# SOLUTION
# ============================================================================

def filter_active_users_18plus(users):
    """
    Filter users using dictionary comprehension.
    
    Creates a mapping of username → email for users who are:
    1. Active (active == True)
    2. At least 18 years old (age >= 18)
    
    Args:
        users: List of dictionaries with user information
        
    Returns:
        Dictionary mapping username to email for eligible users
    """
    return {user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}


# ============================================================================
# TEST DATA
# ============================================================================

users = [
    {"username": "alice", "email": "a@b.com", "age": 25, "active": True},
    {"username": "bob", "email": "b@b.com", "age": 17, "active": True},
    {"username": "carol", "email": "c@b.com", "age": 30, "active": False},
    {"username": "dave", "email": "d@b.com", "age": 22, "active": True},
]


# ============================================================================
# TESTS
# ============================================================================

def test_filter_active_users_18plus():
    """Test the dictionary comprehension filter."""
    result = filter_active_users_18plus(users)
    
    # Expected output
    expected = {"alice": "a@b.com", "dave": "d@b.com"}
    
    # Assertions
    assert result == expected, f"Expected {expected}, got {result}"
    assert len(result) == 2, f"Expected 2 users, got {len(result)}"
    assert "alice" in result, "alice should be in result"
    assert "dave" in result, "dave should be in result"
    assert "bob" not in result, "bob should NOT be in result (age < 18)"
    assert "carol" not in result, "carol should NOT be in result (active=False)"
    
    # Verify values
    assert result["alice"] == "a@b.com", "alice's email incorrect"
    assert result["dave"] == "d@b.com", "dave's email incorrect"
    
    print("✅ All assertions passed!")
    return result


def test_edge_cases():
    """Test edge cases for the dictionary comprehension."""
    
    # Empty list
    result = filter_active_users_18plus([])
    assert result == {}, "Empty list should return empty dict"
    print("✅ Empty list test passed")
    
    # All inactive
    inactive_users = [
        {"username": "user1", "email": "1@b.com", "age": 25, "active": False},
        {"username": "user2", "email": "2@b.com", "age": 30, "active": False},
    ]
    result = filter_active_users_18plus(inactive_users)
    assert result == {}, "All inactive users should return empty dict"
    print("✅ All inactive users test passed")
    
    # All minors
    minor_users = [
        {"username": "user1", "email": "1@b.com", "age": 10, "active": True},
        {"username": "user2", "email": "2@b.com", "age": 17, "active": True},
    ]
    result = filter_active_users_18plus(minor_users)
    assert result == {}, "All minors should return empty dict"
    print("✅ All minors test passed")
    
    # Boundary case: exactly 18
    boundary_users = [
        {"username": "user1", "email": "1@b.com", "age": 18, "active": True},
    ]
    result = filter_active_users_18plus(boundary_users)
    assert result == {"user1": "1@b.com"}, "Age 18 should be included"
    print("✅ Boundary case (age=18) test passed")
    
    # All eligible
    all_eligible = [
        {"username": "user1", "email": "1@b.com", "age": 25, "active": True},
        {"username": "user2", "email": "2@b.com", "age": 30, "active": True},
        {"username": "user3", "email": "3@b.com", "age": 20, "active": True},
    ]
    result = filter_active_users_18plus(all_eligible)
    assert len(result) == 3, "All users should be eligible"
    print("✅ All eligible test passed")


def test_comprehension_one_liner():
    """Verify the comprehension is truly one line."""
    # One-liner version (without function wrapping)
    result = {user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}
    expected = {"alice": "a@b.com", "dave": "d@b.com"}
    
    assert result == expected, f"One-liner failed: {result}"
    print("✅ One-liner comprehension test passed")


# ============================================================================
# DETAILED ANALYSIS
# ============================================================================

def analyze_comprehension():
    """Analyze what the comprehension does step by step."""
    
    print("\n" + "=" * 70)
    print("DICTIONARY COMPREHENSION ANALYSIS")
    print("=" * 70)
    
    print("\nComprehension:")
    print("-" * 70)
    print("{user['username']: user['email']} for user in users if user['active'] and user['age'] >= 18")
    
    print("\nBreakdown:")
    print("-" * 70)
    print("1. KEY: user['username']")
    print("   - Extracts the username as the dictionary key")
    print("2. VALUE: user['email']")
    print("   - Extracts the email as the dictionary value")
    print("3. ITERABLE: for user in users")
    print("   - Iterates through each user dictionary in the list")
    print("4. CONDITION: if user['active'] and user['age'] >= 18")
    print("   - Filters to include only user if BOTH conditions are true:")
    print("     a) user['active'] == True")
    print("     b) user['age'] >= 18")
    
    print("\nProcessing Each User:")
    print("-" * 70)
    
    for user in users:
        username = user["username"]
        email = user["email"]
        age = user["age"]
        active = user["active"]
        
        condition1 = active
        condition2 = age >= 18
        both_true = condition1 and condition2
        
        status = "✅ INCLUDED" if both_true else "❌ EXCLUDED"
        reason = []
        if not condition1:
            reason.append("not active")
        if not condition2:
            reason.append(f"age {age} < 18")
        
        reason_str = f" ({', '.join(reason)})" if reason else ""
        
        print(f"{username:.<20} {email:.<15} age {age:>2} active={active:5} {status}{reason_str}")
    
    print("\n" + "-" * 70)
    print("Result:")
    result = {user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}
    for username, email in result.items():
        print(f"  {username:.<20} {email}")


# ============================================================================
# EQUIVALENT APPROACHES
# ============================================================================

def equivalent_approach_1_filter_function():
    """Equivalent using filter() function."""
    return dict(
        (user["username"], user["email"]) 
        for user in filter(lambda u: u["active"] and u["age"] >= 18, users)
    )


def equivalent_approach_2_list_comprehension_then_dict():
    """Equivalent using list comprehension then dict conversion."""
    filtered_pairs = [(user["username"], user["email"]) for user in users if user["active"] and user["age"] >= 18]
    return dict(filtered_pairs)


def equivalent_approach_3_traditional_loop():
    """Equivalent using traditional for loop."""
    result = {}
    for user in users:
        if user["active"] and user["age"] >= 18:
            result[user["username"]] = user["email"]
    return result


def test_equivalence():
    """Verify all approaches produce the same result."""
    
    comprehension = {user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}
    filter_func = equivalent_approach_1_filter_function()
    list_comp = equivalent_approach_2_list_comprehension_then_dict()
    loop = equivalent_approach_3_traditional_loop()
    
    assert comprehension == filter_func, "Filter approach differs"
    assert comprehension == list_comp, "List comprehension approach differs"
    assert comprehension == loop, "Traditional loop approach differs"
    
    print("✅ All approaches are equivalent!")
    print(f"   Result: {comprehension}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Q18 - FILTER AND TRANSFORM WITH DICTIONARY COMPREHENSION")
    print("=" * 70)
    
    # Test the main solution
    print("\n[Test 1] Main Solution")
    print("-" * 70)
    result = test_filter_active_users_18plus()
    print(f"Result: {result}")
    
    # Test edge cases
    print("\n[Test 2] Edge Cases")
    print("-" * 70)
    test_edge_cases()
    
    # Test one-liner
    print("\n[Test 3] One-Liner Comprehension")
    print("-" * 70)
    test_comprehension_one_liner()
    
    # Analyze the comprehension
    analyze_comprehension()
    
    # Test equivalence
    print("\n[Test 4] Equivalence with Other Approaches")
    print("-" * 70)
    test_equivalence()
    
    print("\n" + "=" * 70)
    print("✅ Q18 - ALL TESTS PASSED!")
    print("=" * 70)
    
    print("\nDICTIONARY COMPREHENSION SYNTAX:")
    print("-" * 70)
    print("{key_expr: value_expr for item in iterable if condition}")
    
    print("\nOUR SOLUTION:")
    print("-" * 70)
    print("{user['username']: user['email'] for user in users if user['active'] and user['age'] >= 18}")
    
    print("\n" + "=" * 70)
