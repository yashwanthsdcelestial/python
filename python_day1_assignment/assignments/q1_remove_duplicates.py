# Q1: Remove Duplicates While Preserving Order
# We cannot use set(), so we manually track what we've already seen

nums = [1, 2, 2, 3, 4, 4, 5]

seen = {}         # Dictionary to track numbers we've already added
result = []       # Final list without duplicates

for num in nums:
    if num not in seen:       # If we haven't seen this number before
        seen[num] = True      # Mark it as seen
        result.append(num)    # Add it to our result

print("Output:", result)
# Output: [1, 2, 3, 4, 5]
