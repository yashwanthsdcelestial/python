# Q2: Second Largest Unique Element
# We cannot use sorting, so we loop through the list and track top two values

nums = [10, 20, 4, 45, 99, 99]

largest = None         # Will hold the biggest number
second_largest = None  # Will hold the second biggest number

for num in nums:
    if largest is None or num > largest:
        # Found a new biggest number
        second_largest = largest   # Old largest becomes second
        largest = num
    elif num != largest:           # Ignore duplicates of the largest
        if second_largest is None or num > second_largest:
            second_largest = num   # Update second largest

print("Output:", second_largest)
# Output: 45
