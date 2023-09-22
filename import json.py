import json

# Open the JSON file
with open('models.json', 'r') as f:
    # Load the JSON data from the file
    data = json.load(f)

# Print the data
print(data)