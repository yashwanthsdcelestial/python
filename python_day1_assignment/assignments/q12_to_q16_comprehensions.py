# Q12: Create Dictionary from Two Lists
# Use dictionary comprehension to map keys to values

keys = ['a', 'b', 'c']
values = [1, 2, 3]

# Dictionary comprehension: {key: value for key, value in zip(keys, values)}
# zip() pairs up elements from two lists: ('a',1), ('b',2), ('c',3)
result = {key: value for key, value in zip(keys, values)}

print("Q12 Output:", result)
# Output: {'a': 1, 'b': 2, 'c': 3}


# -------------------------------------------------------

# Q13: Invert Dictionary Using Comprehension
# Swap keys and values

original = {'a': 1, 'b': 2, 'c': 3}

# Swap key and value positions
inverted = {value: key for key, value in original.items()}

print("Q13 Output:", inverted)
# Output: {1: 'a', 2: 'b', 3: 'c'}


# -------------------------------------------------------

# Q14: Extract Words Starting with Vowel
# Case insensitive - so check the lowercase version

sentence = "apple banana orange grape"
words = sentence.split()   # Split into list of words

vowels = "aeiou"

# List comprehension: include word only if its first letter is a vowel
result = [word for word in words if word[0].lower() in vowels]

print("Q14 Output:", result)
# Output: ['apple', 'orange']


# -------------------------------------------------------

# Q15: Replace Negative Numbers with 0
# Use list comprehension with a condition

numbers = [1, -2, 3, -4, 5]

# If number < 0, use 0; otherwise keep the number
result = [0 if num < 0 else num for num in numbers]

print("Q15 Output:", result)
# Output: [1, 0, 3, 0, 5]


# -------------------------------------------------------

# Q16: Multi-condition List Comprehension
# Numbers divisible by both 2 and 3 (i.e., divisible by 6)

result = [num for num in range(1, 20) if num % 2 == 0 and num % 3 == 0]

print("Q16 Output:", result)
# Output: [6, 12, 18]
