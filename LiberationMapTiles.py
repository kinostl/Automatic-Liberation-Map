from random import randrange, sample
from RandomName import haiku
from string import ascii_letters

class DungeonNode:
    # will be provided a difficulty
    # will be provided a theme
    # This should probably be taking an EncounterConfig object or something so that I can have things be loaded in
    def __init__(self, encounterConfig, difficulty, _type):
        # needs a name
        self.getEncounter = encounterConfig.getEncounter
        self.reId()
        self.reName()
        self.encounter = []
        self.exits = []
        self.entrances = []
        self.difficulty = difficulty
        self._type = _type # fight, social, or puzzle
        self.title=f'{self.id}({self.name} - {self.difficulty})'

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

    def reId(self):
        self.id=''.join(sample(ascii_letters, k=8))
        pass

    def reName(self):
        self.name=haiku()
        pass

    def addEntrance(self, dungeonNode):
        self.entrances.append(dungeonNode)

    def getConnections(self):
        return set(self.entrances + self.exits)

    def addGenerator(self):
        # generators double as signal nodes
        # each generator is also the key for the current difficulty
        self.generator = self.getEncounter('generator')
        self.title=f'{self.id}({self.name} - {self.difficulty} - Generator)'

    def clearGenerator(self):
        # generators double as signal nodes
        # each generator is also the key for the current difficulty
        del self.generator

    # needs to be told its under the effects of a generator
    # this might turn into an element of the generator type
    # actually the dungeon builder cares about this

    def getExitList(self):
        return list(map(lambda x: f'{self.title} --- {x.title}',self.exits))

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
        self.title=self.name
        self.exits=[]
        self.entrances=[]