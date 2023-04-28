import random, json

from ..entities_templates import Curse


with open('entities/data/items_data.json') as f:
    items_data = json.load(f)

class CursesFactory:
    
    def __init__(self):
        self.red = Curse(
            "self-luminous red",
            items_data["curses"]["self-luminous red"],
            1,
            15,
            20,
        )
        self.hyperbolic_orange = Curse(
            "hyperbolic orange",
            items_data["curses"]["hyperbolic orange"],
            1,
            15,
            20,
        )
        self.stygian_blue = Curse(
            "stygian blue",
            items_data["curses"]["stygian blue"],
            1,
            15,
            20,
        )
        self.discourse = Curse(
            "Discourse on the Method of Rightly Conducting One's Reason and of Seeking Truth in the Sciences",
            items_data["curses"]["method"],
            1,
            15,
            20,
        )
        self.falsidical = Curse(
            "falsidical paradox",
            items_data["curses"]["falsidical"],
            1,
            15,
            20,
        )
        self.cluster_point = Curse(
            "cluster point",
            items_data["curses"]["cluster point"],
            1,
            15,
            20,
        )
        self.aleph = Curse(
            "Aleph Naught",
            items_data["curses"]["aleph"],
            1,
            15,
            20,
        )
        self.logistic_map = Curse(
            "Logistic Map",
            items_data["curses"]["logistic map"],
            1,
            15,
            20,
        )
        self.integral = Curse(
            "integral of a real multivariate function",
            items_data["curses"]["integral"],
            1,
            15,
            20,
        )
        self.veridical = Curse(
            "veridical paradox",
            items_data["curses"]["veridical"],
            1,
            15,
            20,
        )
        self.comic_sans = Curse(
            "Comic Sans",
            items_data["curses"]["comic sans"],
            1,
            15,
            20,
        )
        self.sep = Curse(
            "Somebody Else's Problem Field",
            items_data["curses"]["sep field"],
            1,
            15,
            20,
        )
        self.nimby = Curse(
            "not in my back yard",
            items_data["curses"]["nimby"],
            1,
            15,
            20,
        )
        self.choice = Curse(
            "Axiom of Choice",
            items_data["curses"]["choice"],
            1,
            15,
            20,
        )
        self.antinomy = Curse(
            "antinomy",
            items_data["curses"]["antinomy"],
            1,
            15,
            20,
        )
        self.continuum = Curse(
            "continuum hypothesis",
            items_data["curses"]["continuum"],
            1,
            15,
            20,
        )
        self.insult = Curse(
            "Ultimate Insult",
            items_data["curses"]["insult"],
            1,
            15,
            20,
        )
        self.briefcase = Curse(
            "Marcellus Wallace's briefcase",
            items_data["curses"]["briefcase"],
            1,
            15,
            20,
        )
        self.riemann = Curse(
            "Riemann zeta function",
            items_data["curses"]["riemann"],
            1,
            15,
            20,
        )