# Q5: Word Frequency Counter (File Handling)
# Read a text file, count how many times each word appears
# Rules: ignore case (Hello = hello), ignore punctuation

import string   # Has tools for punctuation

# ---- First, let's create a sample file to test ----
with open("sample.txt", "w") as f:
    f.write("hello world\nhello python")

# ---- Now read and count words ----
word_count = {}   # Dictionary to store word -> count

with open("sample.txt", "r") as file:
    for line in file:
        line = line.lower()   # Convert to lowercase (Hello -> hello)
        
        # Remove punctuation from the line
        for char in string.punctuation:
            line = line.replace(char, "")
        
        words = line.split()   # Split line into individual words
        
        for word in words:
            if word not in word_count:
                word_count[word] = 0
            word_count[word] += 1   # Count the word

print("Output:", word_count)
# Output: {'hello': 2, 'world': 1, 'python': 1}
