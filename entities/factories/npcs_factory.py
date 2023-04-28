from ..entities_templates import NonPlayableCharacter
from .weapons_factory import WeaponsFactory as Wf
from .curses_factory import CursesFactory as Cf
import random, json


with open('entities/data/npcs_data.json') as f:
    npcs_data = json.load(f)


class NPCsFactory:
    
    def __init__(self):
        self.littleo = NonPlayableCharacter(
            "Little(o)",
            npcs_data["littleo"]["description"],
            None,
            1000,
            [Cf().sep, Cf().choice, Cf().riemann]
        )
        self.blacksmith = NonPlayableCharacter(
            "Blacksmith",
            npcs_data["blacksmith"]["description"],
            None,
            1000,
            []
        )
        self.innkeeper = NonPlayableCharacter(
            "innkeeper",
            npcs_data["innkeeper"]["description"],
            None,
            1000,
            []
        )
        self.merchant = NonPlayableCharacter(
            "merchant",
            npcs_data["merchant"]["description"],
            None,
            1000,
            []
        )
        self.monk = NonPlayableCharacter(
            "monk",
            npcs_data["monk"]["description"],
            None,
            1000,
            []
        )
        self.ferns = NonPlayableCharacter(
            "ferns",
            npcs_data["ferns"]["description"],
            None,
            1000,
            []
        )
        self.rina = NonPlayableCharacter(
            "rina",
            npcs_data["rina"]["description"],
            None,
            1000,
            []
        )
        self.intruder = NonPlayableCharacter(
            "intruder",
            npcs_data["intruder"]["description"],
            None,
            1000,
            []
        )
        self.oak = NonPlayableCharacter(
            "oak",
            npcs_data["oak"]["description"],
            None,
            1000,
            []
        )
        self.enzopaolo = NonPlayableCharacter(
            "enzopaolo",
            npcs_data["enzopaolo"]["description"],
            None,
            1000,
            []
        )
        self.priamo = NonPlayableCharacter(
            "priamo",
            npcs_data["priamo"]["description"],
            None,
            1000,
            []
        )
        self.effrafax = NonPlayableCharacter(
            "effrafax",
            npcs_data["effrafax"]["description"],
            None,
            1000,
            []
        )
        self.stylite = NonPlayableCharacter(
            "stylite",
            npcs_data["stylite"]["description"],
            None,
            1000,
            []
        )