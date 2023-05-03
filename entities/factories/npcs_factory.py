from ..entities_templates import NonPlayableCharacter
from .weapons_factory import WeaponsFactory as Wf
from .curses_factory import CursesFactory as Cf
from .healers_factory import HealersFactory as Hf
from .armors_factory import ArmorsFactory as Af


class NPCsFactory:
    
    def __init__(self):
        self.littleo = NonPlayableCharacter(
            "Little(o)",
            1000,
            [Cf().sep, Af().tesla_armor, Cf().choice, Cf().riemann, Wf().poly],
            True
        )
        self.blacksmith = NonPlayableCharacter(
            "Blacksmith",
            1000,
            [Hf().ats],
            True
        )
        self.innkeeper = NonPlayableCharacter(
            "Innkeeper",
            1000,
            [Hf().ats],
            True
        )
        self.merchant = NonPlayableCharacter(
            "Merchant",
            1000,
            [Hf().ats],
            True
        )
        self.monk = NonPlayableCharacter(
            "Monk",
            1000,
            [Hf().ats],
            True
        )
        self.ferns = NonPlayableCharacter(
            "Ferns",
            1000,
            [Hf().ats],
            False
        )
        self.rina = NonPlayableCharacter(
            "Rina",
            1000,
            [Hf().ats],
            False
        )
        self.intruder = NonPlayableCharacter(
            "Intruder",
            1000,
            [Hf().ats],
            False
        )
        self.oak = NonPlayableCharacter(
            "Oak",
            1000,
            [Hf().ats],
            False
        )
        self.enzopaolo = NonPlayableCharacter(
            "Enzo Paolo",
            1000,
            [Hf().ats],
            False
        )
        self.priamo = NonPlayableCharacter(
            "Priamo",
            1000,
            [Hf().ats],
            False
        )
        self.effrafax = NonPlayableCharacter(
            "Effrafax",
            1000,
            [Hf().ats],
            False
        )
        self.stylite = NonPlayableCharacter(
            "Stylite",
            1000,
            [Hf().ats],
            False
        )
        
