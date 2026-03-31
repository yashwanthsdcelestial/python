# Q3: Group Anagrams
# Anagrams are words with the same letters (e.g., "eat", "tea", "ate")
# Trick: If we sort the letters of an anagram, they all become the same word
# "eat" sorted = "aet", "tea" sorted = "aet", "ate" sorted = "aet"

words = ["eat", "tea", "tan", "ate", "nat", "bat"]

groups = {}  # Dictionary: sorted_word -> list of original words

for word in words:
    sorted_word = "".join(sorted(word))   # Sort the letters of the word
    
    if sorted_word not in groups:
        groups[sorted_word] = []          # Create a new group
    
    groups[sorted_word].append(word)      # Add word to its group

# Get just the values (the groups), not the keys
result = list(groups.values())

print("Output:", result)
# Output: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
