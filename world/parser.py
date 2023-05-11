from world.tiles import *
from world.enemies_tiles import *


# >>>> WORLD
# ROW WORLD MAP
world_dsl = """
|  |  |  |  |  |  |  |RV|IN|  |  |  |  |  |  |
|OK|  |  |  |  |  |  |RV|  |  |  |Lo|  |  |  |
|  |.2|..|.2|..|.3|  |RV|  |.3|..|.3|..|.3|  |
|  |.2|  |.1|  |..|  |RV|  |..|  |  |  |.3|  |
|  |.1|  |..|  |.3|  |RV|  |.4|  |  |  |..|  |
|  |.2|  |..|  |.2|  |RV|  |..|  |  |  |.4|  |
|  |..|  |BS|  |..|  |RV|  |.3|  |  |  |..|  |
|  |.2|  |  |  |.3|.4|..|.3|.4|  |  |  |.3|  |
|  |..|  |  |  |  |  |RV|  |  |  |..|  |..|  |
|  |.1|  |  |  |  |  |RV|  |  |  |.4|  |.4|  |
|  |.2|  |  |.1|.1|  |RV|  |  |  |..|  |.4|  |
|  |.1|..|..|.1|.1|  |RV|  |.5|..|..|.5|.4|  |
|  |  |.2|Lo|  |..|  |RV|  |..|  |Lo|  |  |  |
|  |  |.1|  |  |.1|  |RV|  |.5|  |  |  |  |  |
|  |.1|.2|  |FT|..|  |RV|..|..|  |  |  |  |  |
|  |  |.1|  |  |.2|  |RV|  |.5|  |.5|  |  |  |
|SS|..|.1|..|..|.1|  |RV|  |..|..|..|.5|.5|WW|
|  |  |.1|  |  |.1|  |RV|  |  |  |  |  |  |  |
"""


# Domain-Specific language
def is_dsl_valid(dsl):
    """Checks if the given domain-specific language (DSL) string representing game map is valid.

    A valid DSL string must:
    - Contain exactly one '|SS|' and at least one '|WW|'.
    - Have the same number of pipes ('|') in each row.
    - Have at least one row.

    Args:
    - dsl (str): A string representing the game board in DSL format.

    Returns:
    - bool: True if the DSL string is valid, False otherwise.

    """
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
                  "RV": RiverTile,
                  "Lo": LittleoTile,
                  "OK": OakTile,
                  "..": PathTile,
                  "SS": StartTile,
                  "TM": TempleTile,
                  "WW": VictoryTile,
                  "  ": None}

world_map = []
start_tile_location = None


def parse_world_dsl():
    """Parse the given DSL string representing game map, and constructs
    a grid world.

    The DSL string must be a valid game board, satisfying the conditions
    specified in the `is_dsl_valid` function. The constructed world map is a 2D
    list of MapTile objects, where each tile represents a location in the game
    world. The coordinates of a tile within the world map correspond to its x
    and y coordinates on the game board.

    Raises
    ------
    SyntaxError
        If the DSL string is invalid.

    """
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
    """Return MapTile object at the given (x, y) coordinates within the game
    world, if it exists.

    If the given (x, y) location is outside the bounds of the game world
    (i.e., x or y is negative), this function returns None. If the (x, y)
    location is within the bounds of the game world but there is no tile at
    that location, this function also returns None.

    Parameters
    ----------
    x : int
        The x-coordinate of the location to check.
    y : int
        The y-coordinate of the location to check.

    Returns
    -------
    Optional[Tile]
        The Tile object at the given (x, y) coordinates
    None
        If there is no tile at that location.
    """
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None
