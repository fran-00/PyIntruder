from ..entities_templates import Curse


class CursesFactory:
    
    def __init__(self):
        self.red = Curse(
            "Self-Luminous Red",
            15,
            20,
            10
        )
        self.hyperbolic_orange = Curse(
            "Hyperbolic Orange",
            15,
            20,
            10
        )
        self.stygian_blue = Curse(
            "Stygian Blue",
            15,
            20,
            10
        )
        self.discourse = Curse(
            "Discourse on the Method",
            15,
            20,
            10
        )
        self.falsidical = Curse(
            "Falsidical Paradox",
            15,
            20,
            10
        )
        self.cluster_point = Curse(
            "Cluster Point",
            15,
            20,
            10
        )
        self.aleph = Curse(
            "Aleph Naught",
            15,
            20,
            10
        )
        self.logistic_map = Curse(
            "Logistic Map",
            15,
            20,
            10
        )
        self.integral = Curse(
            "Integral Of a Real Multivariate Function",
            15,
            20,
            10
        )
        self.veridical = Curse(
            "Veridical Paradox",
            15,
            20,
            10
        )
        self.comic_sans = Curse(
            "Comic Sans",
            15,
            20,
            10
        )
        self.sep = Curse(
            "Somebody Else's Problem Field",
            15,
            20,
            10
        )
        self.nimby = Curse(
            "NIMBY",
            15,
            20,
            10
        )
        self.choice = Curse(
            "Axiom of Choice",
            15,
            20,
            10
        )
        self.antinomy = Curse(
            "Antinomy",
            15,
            20,
            10
        )
        self.continuum = Curse(
            "Continuum Hypothesis",
            15,
            20,
            10
        )
        self.insult = Curse(
            "Ultimate Insult",
            15,
            20,
            10
        )
        self.briefcase = Curse(
            "Briefcase",
            15,
            20,
            10
        )
        self.riemann = Curse(
            "Riemann zeta function",
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