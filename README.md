# PyIntruder

## How to Play

You can move around the map and interact with game world by entering commands into the text input line at the bottom of the interface.
To move to an adjacent room, simply enter one of the four cardinal points (**N**, **S**, **W**, **E**).

You can see the world map by typing the (**M**) command (it will be shown in the terminal *for now*) and change it in *world.pareser.py* file via the **DSL**.

When player enters a room where there is a living enemy, they will automatically be attacked and can respond with a physical attack (**A**) by using a weapon or by casting a curse (**C**).
Weapon attacks can miss, while curses cannot but each curse cast consumes a varying amount of Mana.

You shall pay attention to your amount of **HP** (**Health Points**) and **MANA**: if **HP** parameter reaches 0, the game is over. If your **MANA** reaches zero, you will no longer be able to cast curses.
With the appropriate command you can consume an item to heal (**HEAL**) yourself or to restore mana (not yet implemented) : while wandering around the map, you may find a lot of useful stuff around you if you take a good look around. You can pick up items from the environment and drop items from your inventory.

If there is an NPC in the room, their presence is signaled and it is possible to talk to them with talk command (**Talk**). If NPC is willing to trade, they announces it and you can choose to Buy, Sell or Quit.

## Game Commands

The recognized commands case insensitive:

- **NORTH**, **SOUTH**, **WEST**, **EAST** - Move to one of the adjacent rooms, if any.
- **DIAGNOSE** - Show informations about the game and the player.
- **LOOK** - Show a description of the current room and tells what items, enemies, or NPCs are in it.
- **LOOK AT** - Show a detailed description of a specified object.
- **INVENTORY** - Show items in Player's inventory
- **ATTACK** - Attack an enemy with a weapon.
- **CURSE** - Cast a curse on an enemy.
- **RUN** - Try to run away from a fight.
- **TALK TO** - Talk with a NPC.
- **TRADE** - Trade with a NPC.
- **GET ITEM** - Get the specified item from the current room.
- **GET FROM LIST** - Display a list of items to collect from the room.
- **DROP ITEM** - Drop an inventory item in the current room.
- **DROP FROM LIST** - Show inventory to choose what to drop.
- **HEAL** - Select an item from inventory to restore HP.
- **OPEN OBJECT** - Open the indicated object if it is openable.
- **MAP** - Show world map.

## Changelog (2020 - 2023)

- [x]: Add MVC architecture to play via PyQt6 GUI instead of using CLI.
- [x]: Add a system of signals and slots to connect model, view and controller.
- [x]: Add a new way to handle game loop using QThread to process user input received from View without breaking it.
- [x]: Update the signal strings parsing system by implementing **regular expressions**.
- [x]: Update NPC creation organization with a better use of **OOP**.
- [x]: Complete refactoring of player.py code, which had very long and unusable methods in the first version of the project.
- [x]: Generalize Player methods code that could be reused: **choose_item()** method in **Player** class must also be usable for pick up, drop and examine actions, as well as to trade with an npc.
- [ ]: Update with improved exception handling: create ad hoc errors to break the game loop or resume it depending on exception's type.
- [ ]: Improve GUI and add menu bar.
- [ ]: Add save and restore functionality. It was present in the original version of the game but the code needs to be adapted to the changes made since then.
- [ ]: The game window divided into at least three parts, one of which will show the description of the current room.
- [ ]: Printout of the world map, which is probably too large to be contained in a signal as a string. Maybe i'll try putting the string into a JSON file.
- [ ]: Text with a color scheme to highlight character names, commands, and more.
- [ ]: An image generated shown in one of the game windows.
- [ ]: Improve algorithms used to calculate item stats so that gameplay is as balanced as possible.

## Notes

On Linux (in my case on Ubuntu 20.04.6 LTS) you will probably encounter this issue:

    qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
    This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
    Available platform plugins are: xcb, linuxfb, offscreen, eglfs, vkkhrdisplay, wayland, wayland-egl, minimal, vnc, minimalegl."

To solve it, run this command:

    sudo apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev