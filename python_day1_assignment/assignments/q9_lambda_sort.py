# Q9: Lambda + Sorting Complex Structure
# Sort a list of dictionaries by the 'age' key
# Lambda is a small anonymous (unnamed) function written in one line

people = [
    {'name': 'A', 'age': 30},
    {'name': 'B', 'age': 20}
]

# sorted() takes a 'key' argument - what to sort by
# lambda person: person['age']  means "for each person, use their age to sort"
sorted_people = sorted(people, key=lambda person: person['age'])

print("Output:", sorted_people)
# Output: [{'name': 'B', 'age': 20}, {'name': 'A', 'age': 30}]
