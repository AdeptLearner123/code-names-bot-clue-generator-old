class Scenario:
    def __init__(self, id, positive, negative, clues=[], nonclues=[]):
        self.id = id
        self.positive = positive
        self.negative = negative
        self.clues = clues
        self.nonclues = nonclues

    @staticmethod
    def from_yaml_obj(obj):
        return Scenario(obj["id"], obj["positive"], obj["negative"], obj["clues"], obj["nonclues"])

    def to_yaml_obj(self):
        return {
            "id": self.id,
            "positive": self.positive,
            "negative": self.negative,
            "clues": self.clues,
            "nonclues": self.nonclues,
        }


class ScenarioSet:
    def __init__(self, scenarios):
        self.scenarios = scenarios

    @staticmethod
    def from_yaml_obj(obj):
        return ScenarioSet(
            [] if obj is None else [Scenario.from_yaml_obj(scenario_obj) for scenario_obj in obj]
        )

    def to_yaml_obj(self):
        return [scenario.to_yaml_obj() for scenario in self.scenarios]
