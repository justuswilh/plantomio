import json

# Open the config.json file
with open('/Users/justuswilhelm/Documents/Autogen Team 1/config.json', 'r') as file:
    data = json.load(file)

# Update the start_date variable
data['plant_config'][0]['start_date'] = '2.2.2024'

# Write the updated data back to the config.json file
with open('/Users/justuswilhelm/Documents/Autogen Team 1/config.json', 'w') as file:
    json.dump(data, file, indent=4)