from ..entities_templates import NonPlayableCharacter
from .weapons_factory import WeaponsFactory as Wf
from .curses_factory import CursesFactory as Cf
from .healers_factory import HealersFactory as Hf
from .armors_factory import ArmorsFactory as Af


class NPCsFactory:
    
    def __init__(self):
        self.littleo = NonPlayableCharacter(
            "Little(o)",
            None,
            1000,
            [Cf().sep, Af().tesla_armor, Cf().choice, Cf().riemann, Wf().poly],
            self.get_random_dialogue("littleo"),
            True
        )
        self.blacksmith = NonPlayableCharacter(
            "Blacksmith",
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("blacksmith"),
            True
        )
        self.innkeeper = NonPlayableCharacter(
            "Innkeeper",
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("innkeeper"),
            True
        )
        self.merchant = NonPlayableCharacter(
            "Merchant",
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("merchant"),
            True
        )
        self.monk = NonPlayableCharacter(
            "Monk",
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("monk"),
            True
        )
        self.ferns = NonPlayableCharacter(
            "Ferns",
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("ferns"),
            False
        )
        self.rina = NonPlayableCharacter(
            "Rina",
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("rina"),
            False
        )
        self.intruder = NonPlayableCharacter(
            "Intruder",
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("intruder"),
            False
        )
        self.oak = NonPlayableCharacter(
            "Oak",
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("oak"),
            False
        )
        self.enzopaolo = NonPlayableCharacter(
            "Enzo Paolo",
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("enzopaolo"),
            False
        )
        self.priamo = NonPlayableCharacter(
            "Priamo",
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("priamo"),
            False
        )
        self.effrafax = NonPlayableCharacter(
            "Effrafax",
            None,
            1000,
            [Hf().ats],
            self.get_random_dialogue("effrafax"),
            False
        )
        self.stylite = NonPlayableCharacter(
            "Stylite",
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