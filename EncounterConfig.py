from random import choice, randrange

theme = '???' #randomly decided
def getEncounter(type):
    if(type == 'alarm'):
        return {
            'theme': 'alarm',
            'style': 'test'
        }
    return str(type)

class EncounterConfig:
    # encounters should be a dictionary of lists.
    # liberation maps expect these values: virus, hazard, alarm, lockbox, generator, boss
    def __init__(self, encounters):
        self.encounters=encounters
        self.encounters['alarm']=[]
        self.alarm = {
            'theme': choice([]), # Like the element or class such as Wrecker this should actually be acquired from the Encounter table now that I think about it.
            'style': choice([]) # Like the "High Alert"
        }
        encounterType = randrange(7)
        # Actually benefit should be a classification of Alarm.
        if encounterType == 6:
            # theres a chance of being a beneficial encounter (1/7)
            self.benefit = getEncounter('benefit')
        self.encounters['benefit']=[]
        self.encounters['lockbox']=[]
        self.encounters['generator']=[]
        self.encounters.update(encounters)

    def getEncounter(self, _type):
        # puzzles can just be hazards ala dimensionalgate
        # hazards can also be triggered battle chips?
        # social can be specific hazards?
        # fights are just the classic viruses

        # benefit can be a hotspot for everyone
        # benefit can be mysterdata for everyone

        # alarm encounters are probably effected by viruses somehow. This usually means inhabiting.
        # return choice(self.encounters[_type])
        return _type

