from world.tiles import *
from world.enemies_tiles import *


# >>>> WORLD
# ROW WORLD MAP
world_dsl = """
|  |  |  |  |  |  |TR|  |  |  |  |  |WW|
|  |  |  |  |  |  |TT|  |  |  |  |  |  |
|  |  |  |  |  |  |Lo|  |  |  |  |  |  |
|.4|.4|.4|.4|OK|FT|SS|.1|.1|.2|.2|.3|.3|
|.4|  |!!|  |.4|  |TM|  |.1|  |!!|  |.3|
|.5|  |!!|  |.5|  |BS|  |.1|  |!!|  |.3|
|.4|  |!!|  |.4|  |SQ|  |.1|  |!!|  |.3|
|.5|  |!!|  |.5|  |RC|  |.1|  |!!|  |.3|
|.5|.5|.5|.5|.5|.5|!!|.1|.1|.2|.2|.3|.3|

"""



"""
|  |  |  |  |TR|  |  |RV|IN|  |  |  |  |  |  |
|OK|  |  |  |TT|  |  |RV|  |  |  |Lo|  |  |  |
|  |.2|..|.2|..|.3|  |RV|  |.3|..|.3|..|.3|  |
|  |.2|  |.V|  |..|  |RV|  |..|  |  |  |.3|  |
|  |.1|  |Vn|  |.3|  |RV|  |.4|  |  |  |..|  |
|  |.2|  |Vs|  |.2|  |RV|  |..|  |  |  |.4|  |
|RC|..|  |BS|  |..|  |RV|  |.3|  |TR|  |..|  |
|  |.2|  |  |  |.3|.4|..|.3|.4|  |TT|  |.3|  |
|  |..|  |  |  |  |  |RV|  |  |  |..|  |..|  |
|  |.1|  |  |  |  |  |RV|  |  |  |.4|  |.4|  |
|  |.2|  |  |.1|.1|  |RV|  |  |  |..|  |.4|  |
|  |.1|..|..|.1|.1|  |RV|  |.5|..|..|.5|.4|  |
|  |  |.2|Lo|  |..|  |RV|  |..|  |Lo|  |  |  |
|  |  |.3|  |  |.1|  |RV|  |.5|  |  |  |  |  |
|  |.3|.2|  |FT|..|  |RV|..|..|  |  |  |  |  |
|  |  |.2|  |  |.2|  |RV|  |.5|  |.5|  |  |  |
|SS|..|.1|..|..|.1|  |RV|  |..|..|..|.5|.5|WW|
|  |  |.1|  |  |.1|  |RV|  |  |  |  |  |  |  |
"""


# Domain-Specific language
def is_dsl_valid(dsl):
    if dsl.count("|SS|") != 1:
        return False
    if dsl.count("|WW|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False
    return True

tile_type_dict = {"BS": BlacksmithTile,
                  "!!": ChestTile,
                  ".1": EnemyTile_1,
                  ".2": EnemyTile_2,
                  ".3": EnemyTile_3,
                  ".4": EnemyTile_4,
                  ".5": EnemyTile_5,
                  "FT": FernsTile,
                  "IN": IntruderTile,
                  "Lo": Little_oTile,
                  "OK": OakTile,
                  "..": PathTile,
                  ".V": PathToVillageTile,
                  "RC": RinaTile,
                  "RV": RiverTile,
                  "SQ": SquareTile,
                  "SS": StartTile,
                  "SY": StyliteTile,
                  "TM": TempleTile,
                  "TT": TavernTile,
                  "TR": TavernRoomTile,
                  "WW": VictoryTile,
                  "Vn": VillageNorthTile,
                  "Vs": VillageSouthTile,
                  "  ": None}

world_map = []
start_tile_location = None

# WORLD CONSTRUCTION
def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)
        world_map.append(row)

def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None

