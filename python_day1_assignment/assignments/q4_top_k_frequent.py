# Q4: Top K Frequent Elements
# We need to find the k most frequent elements
# Step 1: Count frequency of each element using a dictionary
# Step 2: Use bucket sort idea - index = frequency, value = list of numbers

nums = [1, 1, 1, 2, 2, 3]
k = 2

# Step 1: Count how many times each number appears
frequency = {}
for num in nums:
    if num not in frequency:
        frequency[num] = 0
    frequency[num] += 1

# Step 2: Create buckets - bucket[i] contains numbers that appear i times
# Max frequency can be len(nums), so we create that many buckets
buckets = [[] for _ in range(len(nums) + 1)]

for num, count in frequency.items():
    buckets[count].append(num)   # Put number in the bucket matching its count

# Step 3: Collect results from highest frequency bucket downward
result = []
for i in range(len(buckets) - 1, 0, -1):   # Go from high to low
    for num in buckets[i]:
        result.append(num)
        if len(result) == k:                 # Stop when we have k elements
            print("Output:", result)
            exit()

print("Output:", result)
# Output: [1, 2]
