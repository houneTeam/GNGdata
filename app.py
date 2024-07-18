from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import json
import os
from program.conv import convert_theme as convert_theme_data  # Import the convert_theme function

app = Flask(__name__)

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def parse_grid(grid_str, width):
    grid_elements = grid_str.split(',')
    grid_2d = [grid_elements[i:i + width] for i in range(0, len(grid_elements), width)]
    return grid_2d

def formatCellContent(cell):
    content = cell.strip()
    if ':' in content:
        parts = content.split(':')
        return parts[0].strip()
    return content

def create_theme(theme_name):
    themes_directory = 'gamedata'
    new_theme_path = os.path.join(themes_directory, theme_name)
    if not os.path.exists(new_theme_path):
        os.makedirs(new_theme_path)
        initial_data = {
            "BalanceProperties": [
                {
                    "ThemeId": theme_name
                }
            ],
            "Zones": [
                {
                    "Id": "zone1",
                    "WidthCells": 7,
                    "DepthCells": 12,
                    "FogOfWarCheckpoint": 0,
                    "DecoSeed": 0,
                    "RankMultipliers": [
                        {
                            "GenObjectiveSoftCurrencyMultiplier": 1,
                            "MiningSoftCurrencyMultiplier": 0.1,
                            "GachaSoftCurrencyMultNormal": 0.35,
                            "GachaSoftCurrencyMultPremium": 1,
                            "GachaSoftCurrencyMultRare": 1,
                            "MiningLeaderboardCurrencyMultiplier": 1,
                            "GachaLeaderboardCurrencyMultNormal": 1,
                            "GachaLeaderboardCurrencyMultPremium": 1,
                            "GachaLeaderboardCurrencyMultRare": 1,
                            "GachaCardsMultNormal": 0.1,
                            "GachaCardsMultPremium": 1,
                            "GachaCardsMultRare": 1
                        }
                    ],
                    "Grid": ".,.,e:exit:1:scg_m001_exit,.,.,.,.,x:block2x2,.,r:rockonboardingmine1:2,r:rocksoftcurrencysmall:2,.,.,.,.,x:block1x1v6L,r:rockonboardingmine1:1,r:rockonboardingmine1:2,x:block1x2,x:block2x3vR,.,.,.,r:rockonboardingmine1:1,r:rockonboardingmine1:1,.,.,.,.,x:block1x2,r:rockonboardingmine1:1,r:rockonboardingmine1:1,.,.,.,x:waterfall1x4vL,.,.,.,x:block3x3,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,c:spawningcart:1,.,.,.,.,.,.,.,.,.,.,.,.,x:block1x1v4,x:block2x1,.,x:block1x1v2,x:block1x1v5,x:block2x1,."
                }
            ]
        }
        file_path = os.path.join(new_theme_path, 'CombinedGameData.json')
        write_json(file_path, initial_data)

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

@app.route('/update_zone_name/<theme>/<zone_id>', methods=['POST'])
def update_zone_name(theme, zone_id):
    new_zone_name = request.form.get('new_zone_name')
    if new_zone_name:
        file_path = f'gamedata/{theme}/CombinedGameData.json'
        data = read_json(file_path)
        for zone in data["Zones"]:
            if zone["Id"] == zone_id:
                zone["Id"] = new_zone_name
                break
        write_json(file_path, data)
    return redirect(url_for('zone', theme=theme, zone_id=new_zone_name))

@app.route('/add_rows_top/<theme>/<zone_id>', methods=['POST'])
def add_rows_top(theme, zone_id):
    num_rows = int(request.form.get('num_rows'))
    if num_rows > 0:
        file_path = f'gamedata/{theme}/CombinedGameData.json'
        data = read_json(file_path)
        for zone in data["Zones"]:
            if zone["Id"] == zone_id:
                width = zone["WidthCells"]
                new_rows = ['.' for _ in range(width * num_rows)]
                grid_elements = zone["Grid"].split(',')
                updated_grid = ','.join(new_rows + grid_elements)
                zone["Grid"] = updated_grid
                zone["DepthCells"] += num_rows
                break
        write_json(file_path, data)
    return redirect(url_for('zone', theme=theme, zone_id=zone_id))

@app.route('/add_rows_bottom/<theme>/<zone_id>', methods=['POST'])
def add_rows_bottom(theme, zone_id):
    num_rows = int(request.form.get('num_rows'))
    if num_rows > 0:
        file_path = f'gamedata/{theme}/CombinedGameData.json'
        data = read_json(file_path)
        for zone in data["Zones"]:
            if zone["Id"] == zone_id:
                width = zone["WidthCells"]
                new_rows = ['.' for _ in range(width * num_rows)]
                grid_elements = zone["Grid"].split(',')
                updated_grid = ','.join(grid_elements + new_rows)
                zone["Grid"] = updated_grid
                zone["DepthCells"] += num_rows
                break
        write_json(file_path, data)
    return redirect(url_for('zone', theme=theme, zone_id=zone_id))

@app.route('/remove_rows_top/<theme>/<zone_id>', methods=['POST'])
def remove_rows_top(theme, zone_id):
    num_rows = int(request.form.get('num_rows'))
    if num_rows > 0:
        file_path = f'gamedata/{theme}/CombinedGameData.json'
        data = read_json(file_path)
        for zone in data["Zones"]:
            if zone["Id"] == zone_id:
                width = zone["WidthCells"]
                grid_elements = zone["Grid"].split(',')
                if len(grid_elements) >= width * num_rows:
                    updated_grid = grid_elements[width * num_rows:]
                    zone["Grid"] = ','.join(updated_grid)
                    zone["DepthCells"] -= num_rows
                break
        write_json(file_path, data)
    return redirect(url_for('zone', theme=theme, zone_id=zone_id))

@app.route('/remove_rows_bottom/<theme>/<zone_id>', methods=['POST'])
def remove_rows_bottom(theme, zone_id):
    num_rows = int(request.form.get('num_rows'))
    if num_rows > 0:
        file_path = f'gamedata/{theme}/CombinedGameData.json'
        data = read_json(file_path)
        for zone in data["Zones"]:
            if zone["Id"] == zone_id:
                width = zone["WidthCells"]
                grid_elements = zone["Grid"].split(',')
                if len(grid_elements) >= width * num_rows:
                    updated_grid = grid_elements[:-width * num_rows]
                    zone["Grid"] = ','.join(updated_grid)
                    zone["DepthCells"] -= num_rows
                break
        write_json(file_path, data)
    return redirect(url_for('zone', theme=theme, zone_id=zone_id))

@app.route('/add_columns_left/<theme>/<zone_id>', methods=['POST'])
def add_columns_left(theme, zone_id):
    num_columns = int(request.form.get('num_columns'))
    if num_columns > 0:
        file_path = f'gamedata/{theme}/CombinedGameData.json'
        data = read_json(file_path)
        for zone in data["Zones"]:
            if zone["Id"] == zone_id:
                width = zone["WidthCells"]
                height = zone["DepthCells"]
                grid_elements = zone["Grid"].split(',')
                new_grid = []
                for i in range(height):
                    new_grid.extend(['.' for _ in range(num_columns)] + grid_elements[i*width:(i+1)*width])
                zone["Grid"] = ','.join(new_grid)
                zone["WidthCells"] += num_columns
                break
        write_json(file_path, data)
    return redirect(url_for('zone', theme=theme, zone_id=zone_id))

@app.route('/add_columns_right/<theme>/<zone_id>', methods=['POST'])
def add_columns_right(theme, zone_id):
    num_columns = int(request.form.get('num_columns'))
    if num_columns > 0:
        file_path = f'gamedata/{theme}/CombinedGameData.json'
        data = read_json(file_path)
        for zone in data["Zones"]:
            if zone["Id"] == zone_id:
                width = zone["WidthCells"]
                height = zone["DepthCells"]
                grid_elements = zone["Grid"].split(',')
                new_grid = []
                for i in range(height):
                    new_grid.extend(grid_elements[i*width:(i+1)*width] + ['.' for _ in range(num_columns)])
                zone["Grid"] = ','.join(new_grid)
                zone["WidthCells"] += num_columns
                break
        write_json(file_path, data)
    return redirect(url_for('zone', theme=theme, zone_id=zone_id))

@app.route('/remove_columns_left/<theme>/<zone_id>', methods=['POST'])
def remove_columns_left(theme, zone_id):
    num_columns = int(request.form.get('num_columns'))
    if num_columns > 0:
        file_path = f'gamedata/{theme}/CombinedGameData.json'
        data = read_json(file_path)
        for zone in data["Zones"]:
            if zone["Id"] == zone_id:
                width = zone["WidthCells"]
                height = zone["DepthCells"]
                grid_elements = zone["Grid"].split(',')
                if width > num_columns:
                    new_grid = []
                    for i in range(height):
                        new_grid.extend(grid_elements[i*width+num_columns:(i+1)*width])
                    zone["Grid"] = ','.join(new_grid)
                    zone["WidthCells"] -= num_columns
                break
        write_json(file_path, data)
    return redirect(url_for('zone', theme=theme, zone_id=zone_id))

@app.route('/remove_columns_right/<theme>/<zone_id>', methods=['POST'])
def remove_columns_right(theme, zone_id):
    num_columns = int(request.form.get('num_columns'))
    if num_columns > 0:
        file_path = f'gamedata/{theme}/CombinedGameData.json'
        data = read_json(file_path)
        for zone in data["Zones"]:
            if zone["Id"] == zone_id:
                width = zone["WidthCells"]
                height = zone["DepthCells"]
                grid_elements = zone["Grid"].split(',')
                if width > num_columns:
                    new_grid = []
                    for i in range(height):
                        new_grid.extend(grid_elements[i*width:(i+1)*width-num_columns])
                    zone["Grid"] = ','.join(new_grid)
                    zone["WidthCells"] -= num_columns
                break
        write_json(file_path, data)
    return redirect(url_for('zone', theme=theme, zone_id=zone_id))

@app.route('/convert_theme/<theme>', methods=['GET'])
def convert_theme_route(theme):
    file_path = f'gamedata/{theme}/CombinedGameData.json'
    data = read_json(file_path)
    output_json = convert_theme_data(data)
    return jsonify(output_json)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
