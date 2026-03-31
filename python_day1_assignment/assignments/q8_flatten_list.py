# Q8: Flatten Nested List (Recursive)
# Convert a deeply nested list into a flat (single-level) list
# We use recursion - the function calls itself for inner lists

def flatten(nested_list):
    result = []   # This will hold our flat list
    
    for item in nested_list:
        if isinstance(item, list):         # If the item is itself a list...
            flat = flatten(item)           # ...recursively flatten it
            result.extend(flat)            # Add all its elements to result
        else:
            result.append(item)            # If it's a number, just add it
    
    return result

# Test
nested = [1, [2, [3, 4], 5], 6]
output = flatten(nested)
print("Output:", output)
# Output: [1, 2, 3, 4, 5, 6]
