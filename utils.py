# utils.py
import json
import os

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
                    "Grid": ".,.,e:exit:1:scg_m001_exit,.,.,.,.,x:block2x2,.,r:rockonboardingmine1:2,r:rocksoftcurrencysmall:2,.,.,.,.,x:block1x1v6L,r:rockonboardingmine1:1,r:rockonboardingmine1:2,x:block1x2,x:block2x3vR,.,.,.,r:rockonboardingmine1:1,r:rockonboardingmine1:1,.,.,.,.,x:block1x2,r:rockonboardingmine1:1,r:rockonboardingmine1:1,.,.,.,x:waterfall1x4vL,.,.,.,x:block3x3,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,c:spawningcart:1,.,.,.,.,.,.,.,.,.,.,.,.,x:block1x1v4,x:block2x1,.,x:block1x1v2,x:block1x1v5,x:block2x1,."
                }
            ]
        }
        file_path = os.path.join(new_theme_path, 'CombinedGameData.json')
        write_json(file_path, initial_data)
