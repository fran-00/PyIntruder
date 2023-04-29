from ..entities_templates import NonPlayableCharacter
from .weapons_factory import WeaponsFactory as Wf
from .curses_factory import CursesFactory as Cf
from .healers_factory import HealersFactory as Hf
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
            [Cf().sep, Cf().choice, Cf().riemann],
            self.get_random_dialogue("littleo"),
            True
        )
        self.blacksmith = NonPlayableCharacter(
            "Blacksmith",
            npcs_data["blacksmith"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("blacksmith"),
            False
        )
        self.innkeeper = NonPlayableCharacter(
            "innkeeper",
            npcs_data["innkeeper"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("innkeeper"),
            True
        )
        self.merchant = NonPlayableCharacter(
            "merchant",
            npcs_data["merchant"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("merchant"),
            False
        )
        self.monk = NonPlayableCharacter(
            "monk",
            npcs_data["monk"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("monk"),
            False
        )
        self.ferns = NonPlayableCharacter(
            "ferns",
            npcs_data["ferns"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("ferns"),
            False
        )
        self.rina = NonPlayableCharacter(
            "rina",
            npcs_data["rina"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("rina"),
            False
        )
        self.intruder = NonPlayableCharacter(
            "intruder",
            npcs_data["intruder"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("intruder"),
            False
        )
        self.oak = NonPlayableCharacter(
            "oak",
            npcs_data["oak"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("oak"),
            False
        )
        self.enzopaolo = NonPlayableCharacter(
            "enzopaolo",
            npcs_data["enzopaolo"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("enzopaolo"),
            False
        )
        self.priamo = NonPlayableCharacter(
            "priamo",
            npcs_data["priamo"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("priamo"),
            False
        )
        self.effrafax = NonPlayableCharacter(
            "effrafax",
            npcs_data["effrafax"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("effrafax"),
            False
        )
        self.stylite = NonPlayableCharacter(
            "stylite",
            npcs_data["stylite"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("stylite"),
            False
        )
        
    def get_random_dialogue(self, npc_name=str):
        with open('entities/data/npcs_data.json') as f:
            data = json.load(f)
            dialogues = data[npc_name]['dialogues']
            dialogue = random.choice(list(dialogues.values()))
            return dialogue