from flask import Flask, render_template, request
import json
import os

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

# Function to format cell content
def formatCellContent(cell):
    content = cell.strip()
    if ':' in content:
        parts = content.split(':')
        return parts[0].strip()  # Return the part before the colon
    return content

@app.route('/')
def home():
    # Directory path where themes are located
    themes_directory = 'gamedata'

    # List all directories in themes_directory
    theme_list = [name for name in os.listdir(themes_directory) if os.path.isdir(os.path.join(themes_directory, name))]

    # Get selected theme from query parameters or default to 'christmas'
    selected_theme = request.args.get('theme', 'christmas')

    # Construct file path based on selected theme
    file_path = f'{themes_directory}/{selected_theme}/CombinedGameData.json'
    
    # Load the JSON data
    data = read_json(file_path)
    
    # Extract the ThemeId from BalanceProperties
    theme_id = data.get('BalanceProperties', [{}])[0].get('ThemeId', 'Unknown Theme')
    
    # Extract all zones
    zones = data.get('Zones', [])
    
    # Prepare to store parsed grids
    all_grids = []
    
    # Iterate through all zones
    for zone in zones:
        grid_str = zone.get('Grid', '')
        zone_id = zone.get('Id', 'Unknown Zone')
        width = zone.get('WidthCells', 7)
        
        # Parse the grid if it exists
        if grid_str:
            grid_2d = parse_grid(grid_str, width)
        else:
            grid_2d = []
        
        # Append the parsed grid to the list
        all_grids.append({
            'zone_id': zone_id,
            'grid': grid_2d
        })
    
    # Render the template with the theme and grid information
    return render_template('index.html', theme_list=theme_list, selected_theme=selected_theme, theme_id=theme_id, all_grids=all_grids, formatCellContent=formatCellContent)
if __name__ == "__main__":
    app.run(debug=True)