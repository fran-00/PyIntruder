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
            True
        )
        self.blacksmith = NonPlayableCharacter(
            "Blacksmith",
            None,
            1000,
            [Hf().ats],
            True
        )
        self.innkeeper = NonPlayableCharacter(
            "Innkeeper",
            None,
            1000,
            [Hf().ats],
            True
        )
        self.merchant = NonPlayableCharacter(
            "Merchant",
            None,
            1000,
            [Hf().ats],
            True
        )
        self.monk = NonPlayableCharacter(
            "Monk",
            None,
            1000,
            [Hf().ats],
            True
        )
        self.ferns = NonPlayableCharacter(
            "Ferns",
            None,
            1000,
            [Hf().ats],
            False
        )
        self.rina = NonPlayableCharacter(
            "Rina",
            None,
            1000,
            [Hf().ats],
            False
        )
        self.intruder = NonPlayableCharacter(
            "Intruder",
            None,
            1000,
            [Hf().ats],
            False
        )
        self.oak = NonPlayableCharacter(
            "Oak",
            None,
            1000,
            [Hf().ats],
            False
        )
        self.enzopaolo = NonPlayableCharacter(
            "Enzo Paolo",
            None,
            1000,
            [Hf().ats],
            False
        )
        self.priamo = NonPlayableCharacter(
            "Priamo",
            None,
            1000,
            [Hf().ats],
            False
        )
        self.effrafax = NonPlayableCharacter(
            "Effrafax",
            None,
            1000,
            [Hf().ats],
            False
        )
        self.stylite = NonPlayableCharacter(
            "Stylite",
            None,
            1000,
            [Hf().ats],
            False
        )
        
