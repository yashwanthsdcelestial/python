"""
Q18 - Practical Examples and Use Cases of Dictionary Comprehensions
===================================================================
"""


# ============================================================================
# PRACTICAL EXAMPLES
# ============================================================================

print("\n" + "=" * 80)
print("PRACTICAL EXAMPLES OF DICTIONARY COMPREHENSIONS")
print("=" * 80)


# Example 1: Filter and Transform User Data
print("\n[Example 1] Original Problem - Filter Active Users 18+")
print("-" * 80)

users = [
    {"username": "alice", "email": "a@b.com", "age": 25, "active": True},
    {"username": "bob", "email": "b@b.com", "age": 17, "active": True},
    {"username": "carol", "email": "c@b.com", "age": 30, "active": False},
    {"username": "dave", "email": "d@b.com", "age": 22, "active": True},
]

active_adults = {u["username"]: u["email"] for u in users if u["active"] and u["age"] >= 18}
print(f"Result: {active_adults}")
print(f"Explanation: Only alice and dave are both active AND 18+ years old")


# Example 2: Create and Filter Product Dictionary
print("\n[Example 2] E-commerce - Filter In-Stock Products by Price")
print("-" * 80)

products = [
    {"id": 1, "name": "Laptop", "price": 999, "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 25, "in_stock": True},
    {"id": 3, "name": "Monitor", "price": 299, "in_stock": False},
    {"id": 4, "name": "Keyboard", "price": 79, "in_stock": True},
    {"id": 5, "name": "Headphones", "price": 149, "in_stock": True},
]

# Get product name mapped to price for items in stock and under $150
affordable_available = {p["name"]: p["price"] for p in products if p["in_stock"] and p["price"] < 150}
print(f"Result: {affordable_available}")


# Example 3: Map Student IDs to GPAs (Filter by Minimum GPA)
print("\n[Example 3] Academic - Map High Performers (GPA > 3.5)")
print("-" * 80)

students = [
    {"id": "S001", "name": "Emma", "gpa": 3.8},
    {"id": "S002", "name": "Liam", "gpa": 3.2},
    {"id": "S003", "name": "Sophia", "gpa": 3.9},
    {"id": "S004", "name": "Noah", "gpa": 3.1},
    {"id": "S005", "name": "Olivia", "gpa": 3.7},
]

honor_students = {s["id"]: s["gpa"] for s in students if s["gpa"] > 3.5}
print(f"Result: {honor_students}")


# Example 4: Filter Employee Records
print("\n[Example 4] HR - Map Employee IDs to Salaries (Active, Salary > $50k)")
print("-" * 80)

employees = [
    {"emp_id": "E001", "name": "Alice Johnson", "salary": 65000, "active": True},
    {"emp_id": "E002", "name": "Bob Smith", "salary": 45000, "active": True},
    {"emp_id": "E003", "name": "Carol White", "salary": 75000, "active": False},
    {"emp_id": "E004", "name": "Dave Brown", "salary": 55000, "active": True},
]

high_earners = {e["emp_id"]: e["salary"] for e in employees if e["active"] and e["salary"] > 50000}
print(f"Result: {high_earners}")


# Example 5: Filter Social Media Posts
print("\n[Example 5] Social Media - Map Post IDs to Engagement (100+ likes, Published)")
print("-" * 80)

posts = [
    {"id": "P001", "title": "Python Tips", "likes": 250, "published": True},
    {"id": "P002", "title": "Draft Post", "likes": 50, "published": False},
    {"id": "P003", "title": "JavaScript Guide", "likes": 180, "published": True},
    {"id": "P004", "title": "Another Draft", "likes": 30, "published": False},
    {"id": "P005", "title": "Web Design", "likes": 95, "published": True},
]

viral_posts = {p["id"]: p["likes"] for p in posts if p["published"] and p["likes"] >= 100}
print(f"Result: {viral_posts}")


# ============================================================================
# FILTER CONDITIONS - COMMON PATTERNS
# ============================================================================

print("\n" + "=" * 80)
print("COMMON FILTER PATTERNS")
print("=" * 80)


# Pattern 1: Simple Boolean Filter
print("\n[Pattern 1] Simple Boolean Filter")
print("-" * 80)

items = [{"name": "A", "active": True}, {"name": "B", "active": False}, {"name": "C", "active": True}]
result = {i["name"]: True for i in items if i["active"]}
print(f"Filter: if item['active']")
print(f"Result: {result}")


# Pattern 2: Numeric Range Filter
print("\n[Pattern 2] Numeric Range Filter")
print("-" * 80)

items = [{"id": 1, "score": 45}, {"id": 2, "score": 75}, {"id": 3, "score": 95}, {"id": 4, "score": 55}]
result = {i["id"]: i["score"] for i in items if 60 <= i["score"] <= 90}
print(f"Filter: if 60 <= score <= 90")
print(f"Result: {result}")


# Pattern 3: String Pattern Filter
print("\n[Pattern 3] String Pattern Filter")
print("-" * 80)

items = [{"user": "alice@gmail.com"}, {"user": "bob@company.com"}, {"user": "carol@gmail.com"}]
result = {i["user"].split("@")[0]: i["user"] for i in items if "@gmail.com" in i["user"]}
print(f"Filter: if '@gmail.com' in email")
print(f"Result: {result}")


# Pattern 4: Multiple Conditions (AND)
print("\n[Pattern 4] Multiple Conditions (AND)")
print("-" * 80)

items = [
    {"id": 1, "available": True, "price": 100},
    {"id": 2, "available": False, "price": 50},
    {"id": 3, "available": True, "price": 75},
]
result = {i["id"]: i["price"] for i in items if i["available"] and i["price"] > 80}
print(f"Filter: if available AND price > 80")
print(f"Result: {result}")


# Pattern 5: Multiple Conditions (OR)
print("\n[Pattern 5] Multiple Conditions (OR)")
print("-" * 80)

items = [
    {"id": 1, "priority": "high", "urgent": False},
    {"id": 2, "priority": "low", "urgent": True},
    {"id": 3, "priority": "high", "urgent": True},
    {"id": 4, "priority": "low", "urgent": False},
]
result = {i["id"]: i["priority"] for i in items if i["priority"] == "high" or i["urgent"]}
print(f"Filter: if priority == 'high' OR urgent")
print(f"Result: {result}")


# Pattern 6: Negation (NOT)
print("\n[Pattern 6] Negation (NOT)")
print("-" * 80)

items = [
    {"id": 1, "banned": False},
    {"id": 2, "banned": True},
    {"id": 3, "banned": False},
]
result = {i["id"]: "active" for i in items if not i["banned"]}
print(f"Filter: if not banned")
print(f"Result: {result}")


# ============================================================================
# VALUE TRANSFORMATIONS
# ============================================================================

print("\n" + "=" * 80)
print("VALUE TRANSFORMATIONS IN COMPREHENSIONS")
print("=" * 80)


# Transform 1: String Operations
print("\n[Transform 1] String Operations (Uppercase)")
print("-" * 80)

users = [
    {"username": "alice", "email": "a@b.com", "active": True},
    {"username": "bob", "email": "b@b.com", "active": False},
]
result = {u["username"]: u["email"].upper() for u in users if u["active"]}
print(f"Result: {result}")


# Transform 2: Mathematical Operations
print("\n[Transform 2] Mathematical Operations (Discount Calculation)")
print("-" * 80)

items = [
    {"name": "Item A", "price": 100},
    {"name": "Item B", "price": 50},
]
result = {i["name"]: i["price"] * 0.9 for i in items}  # 10% discount
print(f"Result: {result}")
print(f"Explanation: Each price is multiplied by 0.9 (10% discount)")


# Transform 3: Nested Values (Extract from Nested Dict)
print("\n[Transform 3] Nested Values")
print("-" * 80)

users = [
    {"username": "alice", "contact": {"email": "a@b.com", "phone": "123-456"}},
    {"username": "bob", "contact": {"email": "b@b.com", "phone": "789-012"}},
]
result = {u["username"]: u["contact"]["email"] for u in users}
print(f"Result: {result}")


# Transform 4: Value Type Conversion
print("\n[Transform 4] Type Conversion (String to Float)")
print("-" * 80)

items = [
    {"id": "001", "temp": "25.5"},
    {"id": "002", "temp": "30.2"},
]
result = {i["id"]: float(i["temp"]) for i in items}
print(f"Result: {result}")


# Transform 5: Conditional Value (Ternary Operator)
print("\n[Transform 5] Conditional Value (If-Else in Value)")
print("-" * 80)

students = [
    {"id": "S001", "gpa": 3.8},
    {"id": "S002", "gpa": 2.9},
    {"id": "S003", "gpa": 3.5},
]
result = {s["id"]: "Honor Student" if s["gpa"] >= 3.5 else "Regular Student" for s in students}
print(f"Result: {result}")


# Transform 6: List/Tuple Value
print("\n[Transform 6] Complex Value (Tuple)")
print("-" * 80)

data = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
]
result = {d["id"]: (d["name"], d["age"]) for d in data}
print(f"Result: {result}")


# ============================================================================
# REAL-WORLD SCENARIOS
# ============================================================================

print("\n" + "=" * 80)
print("REAL-WORLD SCENARIOS")
print("=" * 80)


# Scenario 1: API Response Processing
print("\n[Scenario 1] API Response - Extract Valid User IDs")
print("-" * 80)

api_response = {
    "users": [
        {"id": 101, "name": "Alice", "verified": True},
        {"id": 102, "name": "Bob", "verified": False},
        {"id": 103, "name": "Carol", "verified": True},
        {"id": 104, "name": "Dave", "verified": False},
    ]
}

verified_user_ids = {
    u["id"]: u["name"] 
    for u in api_response["users"] 
    if u["verified"]
}
print(f"Result: {verified_user_ids}")
print(f"Explanation: Only verified users are included")


# Scenario 2: Database Query Result Filtering
print("\n[Scenario 2] Database Results - Active Customers > $1000 Lifetime Value")
print("-" * 80)

db_customers = [
    {"cust_id": "C001", "name": "Apple Inc", "lifetime_value": 5000, "status": "active"},
    {"cust_id": "C002", "name": "Small Shop", "lifetime_value": 800, "status": "active"},
    {"cust_id": "C003", "name": "Big Corp", "lifetime_value": 15000, "status": "inactive"},
    {"cust_id": "C004", "name": "Medium Co", "lifetime_value": 2000, "status": "active"},
]

high_value_active = {
    c["cust_id"]: c["lifetime_value"]
    for c in db_customers
    if c["status"] == "active" and c["lifetime_value"] > 1000
}
print(f"Result: {high_value_active}")


# Scenario 3: Config File Processing
print("\n[Scenario 3] Config Processing - Enabled Settings Only")
print("-" * 80)

config = {
    "settings": [
        {"key": "debug", "value": True, "enabled": True},
        {"key": "logging", "value": "INFO", "enabled": False},
        {"key": "timeout", "value": 30, "enabled": True},
        {"key": "retry", "value": 3, "enabled": False},
    ]
}

enabled_settings = {
    s["key"]: s["value"]
    for s in config["settings"]
    if s["enabled"]
}
print(f"Result: {enabled_settings}")


# ============================================================================
# PERFORMANCE COMPARISON
# ============================================================================

print("\n" + "=" * 80)
print("PERFORMANCE COMPARISON")
print("=" * 80)

import timeit

# Create test data
test_users = [
    {"username": f"user{i}", "email": f"user{i}@b.com", "age": 20 + (i % 40), "active": i % 2 == 0}
    for i in range(1000)
]

# Method 1: Dictionary Comprehension
def method_comprehension():
    return {u["username"]: u["email"] for u in test_users if u["active"] and u["age"] >= 18}

# Method 2: Traditional For Loop
def method_loop():
    result = {}
    for u in test_users:
        if u["active"] and u["age"] >= 18:
            result[u["username"]] = u["email"]
    return result

# Method 3: Using filter()
def method_filter():
    return dict(
        (u["username"], u["email"]) 
        for u in filter(lambda u: u["active"] and u["age"] >= 18, test_users)
    )

# Run timing tests
comp_time = timeit.timeit(method_comprehension, number=10000)
loop_time = timeit.timeit(method_loop, number=10000)
filter_time = timeit.timeit(method_filter, number=10000)

print(f"Dictionary Comprehension: {comp_time:.4f}s")
print(f"Traditional For Loop:     {loop_time:.4f}s")
print(f"filter() Function:        {filter_time:.4f}s")
print()
print(f"Comprehension is {loop_time/comp_time:.2f}x faster than for loop")
print(f"Comprehension is {filter_time/comp_time:.2f}x faster than filter()")

print("\n" + "=" * 80)
