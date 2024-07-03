![alt text](https://cdn.discordapp.com/attachments/1161307435475148910/1253741774950760498/gob-32.png?ex=6684cd44&is=66837bc4&hm=99d5119e44e2a51d9faab71d5238b76eaf4a18c5cdc06b9d5c8f1e0091d73853&)

# GNG Grid Display

This project is a Flask web application that displays a grid from a JSON data file. The application reads the JSON file, extracts the relevant theme and zone information, and renders a grid on a web page.

![alt text](https://cdn.discordapp.com/attachments/963432936349253672/1257977188368519169/Screenshot_2.png?ex=66865e0d&is=66850c8d&hm=a7d770ea8778f4e8ad6d2f7b1814e6ca36d87abc90a459414abd3c0ee94666a1&)

## Features

- Reads a JSON file containing game data.
- Extracts and displays the theme name and zone ID.
- Displays a grid based on the data from the JSON file.
- Displays various objects on the map including walls, blocks, waterfalls, different types of stones and resources, precious stones, checkpoints, and a starting platform.

## Objects on the Map

- Walls (x:wall1x1vL, x:wall1x1vR)
- Blocks (x:block1x1v1, x:block1x1v2, x:block1x1v3, x:block1x1v4, x:block1x1v5, x:block2x1, x:block2x2)
- Waterfalls (x:waterfall1x4vL, x:waterfall1x4vR)
- Different types of stones and resources (r:rockbasic, r:rocksoftcurrencybig, r:rocksoftcurrencysmall, r:rockleaderboardcurrency, r:rockgachaforged, r:rockgachawooden, r:rockgachairon, r:rockgachascripted, r:rockkey, r:rockonboarding)
- Precious stones (s:tourmaline, s:sapphire, s:onyx, s:jade, s:opal, s:topaz, s:agate, s:citrine, s:amethyst)
- Checkpoints (p:checkpoint)
- Starting platform (c:spawningcart)

## Requirements

- Python 3.10 or later
- Flask 2.0.2 or later
