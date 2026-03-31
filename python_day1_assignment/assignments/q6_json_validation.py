# Q6: JSON Validation
# Check if a string is valid JSON
# We use Python's built-in json module and try-except to catch errors

import json

def is_valid_json(text):
    try:
        json.loads(text)   # Try to parse the string as JSON
        return True        # If no error, it's valid
    except json.JSONDecodeError:
        return False       # If error, it's not valid

# Test 1 - valid JSON
input1 = '{"name": "John", "age": 30}'
print("Output:", is_valid_json(input1))   # True

# Test 2 - invalid JSON
input2 = '{"name": "John", "age": }'
print("Output:", is_valid_json(input2))   # False
