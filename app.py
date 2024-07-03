from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Function to read JSON data from a file
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to convert the grid string into a 2D array
def parse_grid(grid_str, width):
    grid_elements = grid_str.split(',')
    grid_2d = [grid_elements[i:i + width] for i in range(0, len(grid_elements), width)]
    return grid_2d

@app.route('/')
def home():
    # Path to the JSON file
    file_path = r'gamedata\volcano\CombinedGameData.json'
    
    # Load the JSON data
    data = read_json(file_path)
    
    # Extract the ThemeId from BalanceProperties
    try:
        theme_id = data['BalanceProperties'][0]['ThemeId']
    except KeyError:
        theme_id = 'Unknown Theme'
    
    # Extract the first zone
    try:
        zone = data['Zones'][0]
        grid_str = zone['Grid']
        zone_id = zone['Id']
        width = zone['WidthCells']
    except KeyError:
        zone = {}
        grid_str = ''
        zone_id = 'Unknown Zone'
        width = 7
    
    # Parse the grid if it exists
    if grid_str:
        grid_2d = parse_grid(grid_str, width)
    else:
        grid_2d = []
    
    # Render the template with the theme and grid information
    return render_template('index.html', theme_id=theme_id, zone_id=zone_id, grid=grid_2d)

if __name__ == "__main__":
    app.run(debug=True)
