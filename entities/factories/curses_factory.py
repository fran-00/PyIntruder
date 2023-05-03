from ..entities_templates import Curse


class CursesFactory:
    
    def __init__(self):
        self.red = Curse(
            "Self-Luminous Red",
            1,
            15,
            20,
            10
        )
        self.hyperbolic_orange = Curse(
            "Hyperbolic Orange",
            1,
            15,
            20,
            10
        )
        self.stygian_blue = Curse(
            "Stygian Blue",
            1,
            15,
            20,
            10
        )
        self.discourse = Curse(
            "Discourse on the Method",
            1,
            15,
            20,
            10
        )
        self.falsidical = Curse(
            "Falsidical Paradox",
            1,
            15,
            20,
            10
        )
        self.cluster_point = Curse(
            "Cluster Point",
            1,
            15,
            20,
            10
        )
        self.aleph = Curse(
            "Aleph Naught",
            1,
            15,
            20,
            10
        )
        self.logistic_map = Curse(
            "Logistic Map",
            1,
            15,
            20,
            10
        )
        self.integral = Curse(
            "Integral Of a Real Multivariate Function",
            1,
            15,
            20,
            10
        )
        self.veridical = Curse(
            "Veridical Paradox",
            1,
            15,
            20,
            10
        )
        self.comic_sans = Curse(
            "Comic Sans",
            1,
            15,
            20,
            10
        )
        self.sep = Curse(
            "Somebody Else's Problem Field",
            1,
            15,
            20,
            10
        )
        self.nimby = Curse(
            "NIMBY",
            1,
            15,
            20,
            10
        )
        self.choice = Curse(
            "Axiom of Choice",
            1,
            15,
            20,
            10
        )
        self.antinomy = Curse(
            "Antinomy",
            1,
            15,
            20,
            10
        )
        self.continuum = Curse(
            "Continuum Hypothesis",
            1,
            15,
            20,
            10
        )
        self.insult = Curse(
            "Ultimate Insult",
            1,
            15,
            20,
            10
        )
        self.briefcase = Curse(
            "Marcellus Wallace's briefcase",
            1,
            15,
            20,
            10
        )
        self.riemann = Curse(
            "Riemann zeta function",
            1,
            15,
            20,
            10
        )
    
    def get_items_list(self):
        curses_list = [
            self.red,
            self.hyperbolic_orange,
            self.stygian_blue,
            self.falsidical,
            self.cluster_point,
            self.aleph,
            self.logistic_map,
            self.integral,
            self.veridical,
            self.comic_sans,
            self.sep,
            self.nimby,
            self.choice,
            self.antinomy,
            self.continuum,
            self.insult,
            self.briefcase,
            self.riemann
        ]
        return curses_list