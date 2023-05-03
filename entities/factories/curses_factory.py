from ..entities_templates import Curse


class CursesFactory:
    
    def __init__(self):
        self.red = Curse(
            "Self-Luminous Red",
            5
        )
        self.hyperbolic_orange = Curse(
            "Hyperbolic Orange",
            10
        )
        self.stygian_blue = Curse(
            "Stygian Blue",
            15
        )
        self.discourse = Curse(
            "Discourse on the Method",
            20
        )
        self.falsidical = Curse(
            "Falsidical Paradox",
            25
        )
        self.cluster_point = Curse(
            "Cluster Point",
            30
        )
        self.aleph = Curse(
            "Aleph Naught",
            35
        )
        self.logistic_map = Curse(
            "Logistic Map",
            40
        )
        self.integral = Curse(
            "Integral Of a Real Multivariate Function",
            45
        )
        self.veridical = Curse(
            "Veridical Paradox",
            50
        )
        self.comic_sans = Curse(
            "Comic Sans",
            55
        )
        self.sep = Curse(
            "Somebody Else's Problem Field",
            60
        )
        self.nimby = Curse(
            "NIMBY",
            65
        )
        self.choice = Curse(
            "Axiom of Choice",
            70
        )
        self.antinomy = Curse(
            "Antinomy",
            75
        )
        self.continuum = Curse(
            "Continuum Hypothesis",
            80
        )
        self.insult = Curse(
            "Ultimate Insult",
            85
        )
        self.briefcase = Curse(
            "Briefcase",
            90
        )
        self.riemann = Curse(
            "Riemann zeta function",
            95
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