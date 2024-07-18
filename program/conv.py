import json

def convert_grid(grid_string):
    elements = grid_string.split(',')
    grid = []
    for element in elements:
        if element == '.':
            grid.append(None)
        else:
            parts = element.split(':')
            obj = {"Key": parts[0]}
            if len(parts) > 1:
                obj["Id"] = parts[1]
            if len(parts) > 2:
                obj["Level"] = int(parts[2])
            if len(parts) > 3:
                obj["SecondaryId"] = parts[3]
            if len(parts) > 4:
                obj["TertiaryId"] = parts[4]
            if len(parts) > 5:
                obj["TertiaryLevel"] = int(parts[5])
            grid.append(obj)
    return grid

def main():
    # Prompt user for input
    input_string = input("Enter the full JSON string: ")

    # Parse the input string to extract parameters and grid content
    input_data = json.loads(input_string)
    balance_id = input_data["BalanceProperties"][0]["ThemeId"]
    zone_data = input_data["Zones"][0]
    grid_string = zone_data["Grid"]

    # Convert the grid string to a list of dictionaries
    grid_list = convert_grid(grid_string)

    # Create the output JSON
    output_json = {
        "LteWorldModel": {
            "BalanceId": balance_id,
            "WorldType": 1,
            "ZoneModel": {
                "Id": zone_data.get("Id", ""),
                "Width": zone_data.get("WidthCells", 0),
                "Depth": zone_data.get("DepthCells", 0),
                "CurrentTickNumber": 44,
                "ReinforcementsLevel": 1,
                "Grid": grid_list
            }
        }
    }

    # Write the output JSON to a file
    output_file_path = "grid_output.json"
    with open(output_file_path, "w") as output_file:
        json.dump(output_json, output_file, indent=2)

    print(f"Output saved to {output_file_path}")

if __name__ == "__main__":
    main()
