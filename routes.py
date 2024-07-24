# routes.py
import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, jsonify
from utils import read_json, write_json, parse_grid, formatCellContent, create_theme, convert_theme

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    themes_directory = 'gamedata'
    themes = os.listdir(themes_directory)
    themes = [theme for theme in themes if os.path.isdir(os.path.join(themes_directory, theme))]
    return render_template('index.html', themes=themes)

@routes.route('/<theme>')
def theme(theme):
    file_path = f'gamedata/{theme}/CombinedGameData.json'
    data = read_json(file_path)
    return render_template('theme.html', theme=theme, data=data)

@routes.route('/<theme>/<zone_id>')
def zone(theme, zone_id):
    file_path = f'gamedata/{theme}/CombinedGameData.json'
    data = read_json(file_path)
    zone = next((z for z in data["Zones"] if z["Id"] == zone_id), None)
    if zone:
        grid = parse_grid(zone["Grid"], zone["WidthCells"])
        return render_template('zone.html', theme=theme, zone=zone, grid=grid, formatCellContent=formatCellContent)
    return "Zone not found", 404

@routes.route('/create_theme', methods=['POST'])
def create_new_theme():
    theme_name = request.form.get('theme_name')
    if theme_name:
        create_theme(theme_name)
    return redirect(url_for('routes.home'))

@routes.route('/update_zone_name/<theme>/<zone_id>', methods=['POST'])
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
    return redirect(url_for('routes.zone', theme=theme, zone_id=new_zone_name))

@routes.route('/add_rows_top/<theme>/<zone_id>', methods=['POST'])
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
    return redirect(url_for('routes.zone', theme=theme, zone_id=zone_id))

@routes.route('/add_rows_bottom/<theme>/<zone_id>', methods=['POST'])
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
    return redirect(url_for('routes.zone', theme=theme, zone_id=zone_id))

@routes.route('/remove_rows_top/<theme>/<zone_id>', methods=['POST'])
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
    return redirect(url_for('routes.zone', theme=theme, zone_id=zone_id))

@routes.route('/remove_rows_bottom/<theme>/<zone_id>', methods=['POST'])
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
    return redirect(url_for('routes.zone', theme=theme, zone_id=zone_id))

@routes.route('/add_columns_left/<theme>/<zone_id>', methods=['POST'])
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
    return redirect(url_for('routes.zone', theme=theme, zone_id=zone_id))

@routes.route('/add_columns_right/<theme>/<zone_id>', methods=['POST'])
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
    return redirect(url_for('routes.zone', theme=theme, zone_id=zone_id))

@routes.route('/remove_columns_left/<theme>/<zone_id>', methods=['POST'])
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
    return redirect(url_for('routes.zone', theme=theme, zone_id=zone_id))

@routes.route('/remove_columns_right/<theme>/<zone_id>', methods=['POST'])
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
    return redirect(url_for('routes.zone', theme=theme, zone_id=zone_id))

@routes.route('/convert_theme/<theme>', methods=['GET'])
def convert_theme_route(theme):
    file_path = f'gamedata/{theme}/CombinedGameData.json'
    data = read_json(file_path)
    output_json = convert_theme(data)
    output_file_path = f'gamedata/{theme}/ConvertedGameData.json'
    write_json(output_file_path, output_json)
    return jsonify(output_json)

@routes.route('/generate-savedata/<theme>', methods=['GET'])
def generate_savedata(theme):
    # Load the converted game data
    converted_game_data_path = os.path.join('gamedata', theme, 'ConvertedGameData.json')
    with open(converted_game_data_path, 'r') as file:
        converted_game_data = json.load(file)
    
    # Load the base SaveData.json
    with open('SaveData.json', 'r') as file:
        save_data = json.load(file)
    
    # Replace the "LteWorldModel" in SaveData.json with the one from ConvertedGameData.json
    save_data["LteWorldModel"] = converted_game_data["LteWorldModel"]

    # Save the new SaveData.json to the theme directory
    save_data_output_path = os.path.join('gamedata', theme, 'SaveData.json')
    write_json(save_data_output_path, save_data)
    
    return jsonify(save_data)

@routes.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(routes.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')