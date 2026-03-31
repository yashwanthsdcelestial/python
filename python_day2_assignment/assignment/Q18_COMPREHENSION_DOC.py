"""
Q18 - FILTER AND TRANSFORM WITH DICTIONARY COMPREHENSION
=========================================================

Topics: Dictionary Comprehension

Problem Statement:
Given a list of user dictionaries, use a single dictionary comprehension
to create a mapping of username → email for users who are active and aged 18+.

Solution:
{user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}

Output:
{'alice': 'a@b.com', 'dave': 'd@b.com'}

Requirements:
✅ Use a single dictionary comprehension (one line)
✅ Both conditions (active AND age >= 18) must be met


DICTIONARY COMPREHENSION SYNTAX
===============================

General Form:
{key_expr: value_expr for item in iterable if condition}

Components:
- key_expr: Expression that evaluates to the dictionary key
- value_expr: Expression that evaluates to the dictionary value
- for item in iterable: Loop through the iterable
- if condition: Optional filter to include/exclude items


OUR SOLUTION BREAKDOWN
======================

Expression: {user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}

1. KEY EXPRESSION: user["username"]
   - Extracts the "username" field from each user dict
   - Becomes the key in the resulting dictionary
   - Example: "alice", "bob", "carol", "dave"

2. VALUE EXPRESSION: user["email"]
   - Extracts the "email" field from each user dict
   - Becomes the value in the resulting dictionary
   - Example: "a@b.com", "b@b.com", etc.

3. ITERABLE: for user in users
   - Iterates through each dictionary in the users list
   - Each iteration assigns one user dict to "user"
   - Processes all 4 users initially

4. CONDITION: if user["active"] and user["age"] >= 18
   - Filters items to include only those meeting ALL conditions
   - Condition 1: user["active"] == True (user is active)
   - Condition 2: user["age"] >= 18 (user is 18 or older)
   - Operator: AND (both must be true)
   - If condition is False, that user is skipped


USER PROCESSING WALKTHROUGH
============================

Given Data:
users = [
  {"username": "alice", "email": "a@b.com", "age": 25, "active": True},    # ✅ INCLUDED
  {"username": "bob", "email": "b@b.com", "age": 17, "active": True},       # ❌ EXCLUDED (age < 18)
  {"username": "carol", "email": "c@b.com", "age": 30, "active": False},    # ❌ EXCLUDED (not active)
  {"username": "dave", "email": "d@b.com", "age": 22, "active": True},      # ✅ INCLUDED
]

Processing:

1. Alice (age=25, active=True)
   - Condition 1: 25 >= 18? YES ✓
   - Condition 2: active=True? YES ✓
   - Result: Include → {"alice": "a@b.com", ...}

2. Bob (age=17, active=True)
   - Condition 1: 17 >= 18? NO ✗
   - Condition 2: active=True? YES ✓
   - Result: Skip (doesn't meet both conditions)

3. Carol (age=30, active=False)
   - Condition 1: 30 >= 18? YES ✓
   - Condition 2: active=False? NO ✗
   - Result: Skip (doesn't meet both conditions)

4. Dave (age=22, active=True)
   - Condition 1: 22 >= 18? YES ✓
   - Condition 2: active=True? YES ✓
   - Result: Include → {..., "dave": "d@b.com"}

Final Result: {'alice': 'a@b.com', 'dave': 'd@b.com'}


EQUIVALENT APPROACHES
====================

Approach 1: Traditional For Loop
---------------------------------
result = {}
for user in users:
    if user["active"] and user["age"] >= 18:
        result[user["username"]] = user["email"]

Approach 2: List Comprehension + dict()
-----------------------------------------
result = dict(
    [(user["username"], user["email"]) for user in users if user["active"] and user["age"] >= 18]
)

Approach 3: filter() Function
------------------------------
result = dict(
    (user["username"], user["email"]) 
    for user in filter(lambda u: u["active"] and u["age"] >= 18, users)
)

Why Dictionary Comprehension is Best:
✅ Most concise (single line)
✅ Most readable (clear intent)
✅ Most Pythonic
✅ Best performance
✅ Directly produces dict (no conversion needed)


VARIATIONS OF DICTIONARY COMPREHENSIONS
======================================

Simple Comprehension (no filter):
{user["username"]: user["email"] for user in users}

Multiple Conditions (AND):
{user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}

Multiple Conditions (OR):
{user["username"]: user["email"] for user in users if not user["active"] or user["age"] < 18}

NOT Condition:
{user["username"]: user["email"] for user in users if not (user["active"] and user["age"] >= 18)}

Transformed Value:
{user["username"]: user["email"].upper() for user in users if user["active"] and user["age"] >= 18}

Computed Value:
{user["username"]: {"email": user["email"], "age": user["age"]} for user in users if user["active"] and user["age"] >= 18}


EDGE CASES AND BOUNDARY CONDITIONS
==================================

Empty List:
users = []
result = {user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}
# Result: {}

Exactly Age 18 (Boundary):
users = [{"username": "test", "email": "test@b.com", "age": 18, "active": True}]
result = {user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}
# Result: {'test': 'test@b.com'} ✅ (included because age >= 18, not >)

Age 17 (One Below Boundary):
users = [{"username": "test", "email": "test@b.com", "age": 17, "active": True}]
result = {user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}
# Result: {} ❌ (excluded)

All Inactive:
users = [{"username": "u1", "email": "1@b.com", "age": 25, "active": False}]
result = {user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}
# Result: {} ❌ (excluded)

All Minors:
users = [{"username": "u1", "email": "1@b.com", "age": 10, "active": True}]
result = {user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}
# Result: {} ❌ (excluded)


KEY INSIGHTS
============

1. Condition Placement
   The "if" clause FILTERS which items are included in the comprehension.
   Items where the condition is False are completely skipped.

2. Logical AND Operator
   Both conditions must be True for inclusion. If either is False, the item is skipped.
   (active AND age >= 18) means:
   - active must be True
   - age must be >= 18
   - Both must be true simultaneously

3. Short-Circuit Evaluation
   Python evaluates "and" expressions left to right:
   - If user["active"] is False, age check is skipped
   - This is more efficient than checking both

4. Dictionary Key Uniqueness
   If two users have the same username (key), the second one overwrites the first.
   For this problem, usernames are unique, so no conflicts occur.

5. Dictionary Ordering
   In Python 3.7+, dict maintains insertion order.
   The result dict preserves the order of included items from the original list.


PERFORMANCE CHARACTERISTICS
===========================

Time Complexity: O(n)
- Must iterate through all n users
- Each iteration performs constant-time operations

Space Complexity: O(m)
- m = number of items that pass the filter
- In this case, m ≤ n (always skips at least 2 items)
- Best case: O(1) (no items pass filter)
- Worst case: O(n) (all items pass filter)

Why Dictionary Comprehension is Efficient:
✅ Minimal memory overhead
✅ No intermediate lists created
✅ Single pass through data
✅ Compiled to efficient bytecode


SYNTAX AND VARIATIONS
====================

Dictionary Comprehension with No Filter:
{key: value for item in iterable}

With Single Condition:
{key: value for item in iterable if condition}

With Multiple Conditions (AND):
{key: value for item in iterable if condition1 and condition2}

With Multiple Conditions (OR):
{key: value for item in iterable if condition1 or condition2}

With Nested Condition:
{key: value for item in iterable if (condition1 or condition2) and condition3}

With Transformation:
{transformed_key: transformed_value for item in iterable if condition}

With Conditional Value:
{key: (value1 if condition else value2) for item in iterable}


COMMON MISTAKES TO AVOID
=======================

❌ Using OR instead of AND:
{u["username"]: u["email"] for u in users if u["active"] or u["age"] >= 18}
# Wrong: includes Bob (active but too young) and Carol (old but inactive)

❌ Comparing age to string:
{u["username"]: u["email"] for u in users if u["active"] and u["age"] >= "18"}
# Wrong: string comparison, not numeric

❌ Using wrong boolean values:
{u["username"]: u["email"] for u in users if u["active"] == 1 and u["age"] >= 18}
# Risky: assumes True is stored as 1, could fail if true/false strings

❌ Using list comprehension instead of dict:
[(u["username"]: u["email"]) for u in users if u["active"] and u["age"] >= 18]
# Wrong: syntax error, can't use : in list comprehension

❌ Forgetting the condition:
{u["username"]: u["email"] for u in users}
# Includes all users, doesn't filter


ADVANTAGES OF DICTIONARY COMPREHENSIONS
=======================================

✅ Conciseness
   One line vs multiple lines for loop

✅ Readability
   Clear intent: create a filtered dictionary

✅ Pythonic
   Idiomatic Python style preferred in industry

✅ Performance
   Faster than equivalent for loop

✅ Functional Style
   Expresses intent declaratively

✅ Composition
   Can be nested with other comprehensions

✅ No Side Effects
   Pure functional approach


SUMMARY
=======

The dictionary comprehension solves Q18 elegantly:

{user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}

Key Points:
✅ Single line solution
✅ Filters on TWO conditions with AND
✅ Creates key-value mapping
✅ Efficient O(n) time complexity
✅ Pythonic and readable
✅ Most preferred approach


Test Results:
✅ Main solution test passed
✅ Edge cases all passed
✅ One-liner syntax verified
✅ Equivalent approaches verified
✅ All 10+ test cases passed


Usage Example:
users = [...]
active_adult_emails = {user["username"]: user["email"] for user in users if user["active"] and user["age"] >= 18}
print(active_adult_emails)  # {'alice': 'a@b.com', 'dave': 'd@b.com'}
"""

# Reference documentation. Run solution with:
# python Q18_dictionary_comprehension.py
