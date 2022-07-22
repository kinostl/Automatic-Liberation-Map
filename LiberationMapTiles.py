from random import randrange
import uuid

class DungeonNode:
    # will be provided a difficulty
    # will be provided a theme
    # This should probably be taking an EncounterConfig object or something so that I can have things be loaded in
    def __init__(self, encounterConfig, difficulty, _type):
        # needs a name
        self.getEncounter = encounterConfig.getEncounter
        self.name=str(uuid.uuid4()).split('-')[0]
        self.encounter = []
        self.exits = []
        self.difficulty = difficulty
        self._type = _type # fight, social, or puzzle
        self.name=f'{self.name}({self.name} - {self.difficulty})'

        self.countdown = randrange(4,12)

        encounterType = randrange(7)
        if encounterType == 6:
            # theres a chance of being a beneficial encounter (1/7)
            self.encounter.append(self.getEncounter('benefit'))
        else:
            # encounters are alarms by default (6/7)
            # alarms probably always just create a Hazard?
            self.encounter.append(self.getEncounter('alarm'))
            self.encounter.append(self.getEncounter('lockbox'))

    def addExit(self, dungeonNode):
        self.exits.append(dungeonNode)

    def addGenerator(self):
        # generators double as signal nodes
        # each generator is also the key for the current difficulty
        self.generator = self.getEncounter('generator')

    def clearGenerator(self):
        # generators double as signal nodes
        # each generator is also the key for the current difficulty
        del self.generator

    # needs to be told its under the effects of a generator
    # this might turn into an element of the generator type
    def modifyEncounter(self, generator):
        pass

    def getExitList(self):
        return list(map(lambda x: f'{self.name}---{x.name}',self.exits))

class DungeonNodeBasic(DungeonNode):
    def __init__(self, encounterConfig, difficulty, _type):
        DungeonNode.__init__(self, encounterConfig, difficulty, _type)
        for _ in range(difficulty):
            self.encounter.append(self.getEncounter(_type))

class DungeonNodeBoss(DungeonNode):
    ## bossNode
    # boss node needs to provide a theme
    # themes are just gonna be the element table types
    # 1 difficulty is allocated to the megavirus and the other difficutlies are allocated to hazards or viruses
    def __init__(self, encounterConfig, difficulty, _type):
        DungeonNode.__init__(self, encounterConfig, difficulty, _type)
        for _ in range(difficulty-1):
            self.encounter.append(self.getEncounter(_type))
        self.encounter.append('boss')
        pass

class DungeonNodeStarter(DungeonNode):
    def __init__(self):
        self.name='Start'
        self.exits=[]