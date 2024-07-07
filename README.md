# GNG Grid Display

![alt text](https://cdn.discordapp.com/attachments/1161307435475148910/1253741774950760498/gob-32.png?ex=668b64c4&is=668a1344&hm=480e786d2a36daf9df1f1a6b48106e97aeb444d6b1ae2e2a708efc33383c568b&)

This project is a Flask web application that displays a grid from a JSON data file. The application reads the JSON file, extracts the relevant theme and zone information, and renders a grid on a web page.

![alt text](https://cdn.discordapp.com/attachments/1195907205715722380/1259505727345659965/image.png?ex=668bed9d&is=668a9c1d&hm=b76d008fab5dec7cc15c59e647bcef262d22913705620ef0caf76d67b1353372&)

## Features

- Reads a JSON file containing game data.
- Extracts and displays the theme name and zone ID.
- Displays a grid based on the data from the JSON file.
- Displays various objects on the map including walls, blocks, waterfalls, different types of stones and resources, precious stones, checkpoints, and a starting platform.

## Objects on the Map

- Walls (`x:wall1x1vL`, `x:wall1x1vR`)
- Blocks (`x:block1x1v1`, `x:block1x1v2`, `x:block1x1v3`, `x:block1x1v4`, `x:block1x1v5`, `x:block2x1`, `x:block2x2`)
- Waterfalls (`x:waterfall1x4vL`, `x:waterfall1x4vR`)
- Different types of stones and resources (`r:rockbasic`, `r:rocksoftcurrencybig`, `r:rocksoftcurrencysmall`, `r:rockleaderboardcurrency`, `r:rockgachaforged`, `r:rockgachawooden`, `r:rockgachairon`, `r:rockgachascripted`, `r:rockkey`, `r:rockonboarding`)
- Precious stones (`s:tourmaline`, `s:sapphire`, `s:onyx`, `s:jade`, `s:opal`, `s:topaz`, `s:agate`, `s:citrine`, `s:amethyst`)
- Checkpoints (`p:checkpoint`)
- Starting platform (`c:spawningcart`)

## Project Checklist

### Core Components

- [X] Localization Unpacker
- [X] GameData Unpacker
- [X] Web UI
- [ ] Theme Creator


## Requirements

- Python 3.10 or later
- Flask 2.0.2 or later