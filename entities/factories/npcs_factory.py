from ..entities_templates import NonPlayableCharacter
from .weapons_factory import WeaponsFactory as Wf
from .curses_factory import CursesFactory as Cf
from .healers_factory import HealersFactory as Hf
from .armors_factory import ArmorsFactory as Af
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
            [Cf().sep, Af().tesla_armor, Cf().choice, Cf().riemann, Wf().poly],
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
            True
        )
        self.innkeeper = NonPlayableCharacter(
            "Innkeeper",
            npcs_data["innkeeper"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("innkeeper"),
            True
        )
        self.merchant = NonPlayableCharacter(
            "Merchant",
            npcs_data["merchant"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("merchant"),
            True
        )
        self.monk = NonPlayableCharacter(
            "Monk",
            npcs_data["monk"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("monk"),
            True
        )
        self.ferns = NonPlayableCharacter(
            "Ferns",
            npcs_data["ferns"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("ferns"),
            False
        )
        self.rina = NonPlayableCharacter(
            "Rina",
            npcs_data["rina"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("rina"),
            False
        )
        self.intruder = NonPlayableCharacter(
            "Intruder",
            npcs_data["intruder"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("intruder"),
            False
        )
        self.oak = NonPlayableCharacter(
            "Oak",
            npcs_data["oak"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("oak"),
            False
        )
        self.enzopaolo = NonPlayableCharacter(
            "Enzo Paolo",
            npcs_data["enzo paolo"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("enzopaolo"),
            False
        )
        self.priamo = NonPlayableCharacter(
            "Priamo",
            npcs_data["priamo"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("priamo"),
            False
        )
        self.effrafax = NonPlayableCharacter(
            "Effrafax",
            npcs_data["effrafax"]["description"],
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("effrafax"),
            False
        )
        self.stylite = NonPlayableCharacter(
            "Stylite",
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