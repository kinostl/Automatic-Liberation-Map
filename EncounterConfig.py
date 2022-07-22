from random import sample
class Encounter:
    pass

#
class EncounterConfig:
    # encounters should be a dictionary of lists.
    # liberation maps expect these values: virus, hazard, alarm, lockbox, generator, boss
    def __init__(self, encounters):
        self.encounters = encounters

    def getEncounter(self, _type):
        # puzzles can just be hazards ala dimensionalgate
        # hazards can also be triggered battle chips?
        # social can be specific hazards?
        # fights are just the classic viruses

        # benefit can be a hotspot for everyone
        # benefit can be mysterdata for everyone

        # alarm encounters are probably effected by viruses somehow. This usually means inhabiting.
        # encounter = sample(self.encounters[_type],1)[0]
        # return encounter
        return _type
