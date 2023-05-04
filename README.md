# PyIntruder

## How to Play

The player can move around the world map by entering commands into the text input line at the bottom of the interface. You can see the world map by typing the M command (it will be shown in the terminal) and change it to world.pareser.py via the DSL.
The recognized commands case insensitive:

- **N**, **S**, **W**, **O** - Move to one of the adjacent rooms, if any.
- **A**, **ATTACK** - Attack an enemy.
- **C**, **CURSE** - Cast a curse on an enemy.
- **I**, **INVENTORY** - See currently owned items.
- **T**, **TALK** - Talk and trade with an NPC.
- **P**, **PICK UP** - Pick up an item in the current room.
- **D**, **DROP** - Drop an inventory item in the current room.
- **DIAGNOSE** - Provides informations about the game and the player.
- **RUN**, **FLEE**, **ESCAPE**: try to run away from a fight with an enemy.
- **M**, **MAP** - Show world map.

When the player enters a room where there is a living enemy, he will automatically be attacked and can respond with a physical attack by using a weapon or by casting a curse.
Weapon attacks can miss, while curses cannot but each curse cast consumes a varying amount of Mana.

If there is an NPC in the room, his presence is signaled and it is possible to talk to him with TALK command. If the NPC is willing to trade, he announces it and you can choose to Buy, Sell or Quit.

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

