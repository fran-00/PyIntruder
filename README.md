# PyIntruder

## Upcoming Fixes

- Generalize Player methods code that could be reused:
     - **choose_item()** method in **Player** class must also be usable for pick up, drop and examine actions, as well as to trade with an npc.
- Update with improved exception handling: create ad hoc errors to break the game loop or resume it depending on exception's type.

## Upcoming Features

- The game window divided into at least three parts, one of which will show the description of the current room.
- Printout of the world map, which is probably too large to be contained in a signal as a string. Maybe i'll try putting the string into a JSON file.
- Text with a color scheme to highlight character names, commands, and more.
- An image generated shown in one of the game windows, probably via OpenAI API.
- Complete refactoring of player.py code, which has very long and unusable methods in the current version of the project.

