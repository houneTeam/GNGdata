from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random

app = Flask(__name__)

# Function to read JSON data from a file
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to write JSON data to a file
def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Function to convert the grid string into a 2D array
def parse_grid(grid_str, width):
    grid_elements = grid_str.split(',')
    grid_2d = [grid_elements[i:i + width] for i in range(0, len(grid_elements), width)]
    return grid_2d

# Function to format cell content
def formatCellContent(cell):
    content = cell.strip()
    if ':' in content:
        parts = content.split(':')
        return parts[0].strip()  # Return the part before the colon
    return content

# Function to create a new theme
def create_theme(theme_name):
    themes_directory = 'gamedata'
    new_theme_path = os.path.join(themes_directory, theme_name)
    
    # Create the new theme directory if it doesn't exist
    if not os.path.exists(new_theme_path):
        os.makedirs(new_theme_path)
        
        # Create initial CombinedGameData.json with an empty Zone 1
        initial_data = {
            "BalanceProperties": [
                {
                    "ThemeId": theme_name
                }
            ],
            "Zones": [
                {
                    "Id": "Zone 1",
                    "WidthCells": 7,
                    "Grid": generate_grid(7, 7)  # Generate grid for a 7x7 zone
                }
            ]
        }
        
        # Write the initial data to CombinedGameData.json
        file_path = os.path.join(new_theme_path, 'CombinedGameData.json')
        write_json(file_path, initial_data)

# Function to generate a grid string with default levels
def generate_grid(rows, cols):
    elements = [
        'e:exit',
        'x:block1x1v3',
        'x:block2x2v1',
        'r:rockleaderboardcurrency',
        'r:rockbasic',
        'r:rockgachawooden',
        'r:rockkey',
        'r:rocksoftcurrencysmall',
        'r:rocksoftcurrencybig',
        'r:rockgachascripted3',
        'x:waterfall1x4vR',
        's:jade:scg_s10:ca007',
        's:opal:scg_s09:ca006',
        's:topaz:scg_s08:ca005',
        's:agate:GachaIron:ca004',
        'p:checkpoint:scg_c03',
        'c:spawningcart',
        'x:wall1x1vL',
        'x:wall1x1vR'
    ]
    
    def add_default_level(element):
        if ':' in element:
            parts = element.split(':')
            if len(parts) == 2:
                return f"{element}:1"
            return f"{parts[0]}:{parts[1]}:1" + ':'.join(parts[2:])
        return element
    
    grid = [add_default_level(random.choice(elements)) for _ in range(rows * cols)]
    return ','.join(grid)

@app.route('/')
def home():
    themes_directory = 'gamedata'
    themes = os.listdir(themes_directory)
    themes = [theme for theme in themes if os.path.isdir(os.path.join(themes_directory, theme))]
    return render_template('index.html', themes=themes)

@app.route('/<theme>')
def theme(theme):
    file_path = f'gamedata/{theme}/CombinedGameData.json'
    data = read_json(file_path)
    return render_template('theme.html', theme=theme, data=data)

@app.route('/<theme>/<zone_id>')
def zone(theme, zone_id):
    file_path = f'gamedata/{theme}/CombinedGameData.json'
    data = read_json(file_path)
    zone = next((z for z in data["Zones"] if z["Id"] == zone_id), None)
    if zone:
        grid = parse_grid(zone["Grid"], zone["WidthCells"])
        return render_template('zone.html', theme=theme, zone=zone, grid=grid, formatCellContent=formatCellContent)
    return "Zone not found", 404

@app.route('/create_theme', methods=['POST'])
def create_new_theme():
    theme_name = request.form.get('theme_name')
    if theme_name:
        create_theme(theme_name)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
