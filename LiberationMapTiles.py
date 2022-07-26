from __future__ import annotations
from typing import Set
from random import randrange, sample, choice
from RandomName import haiku
from string import ascii_letters
from EncounterConfig import getEncounter
from math import floor
import Encounters

class DungeonNode:
    # will be provided a difficulty
    # will be provided a theme
    # This should probably be taking an EncounterConfig object or something so that I can have things be loaded in
    def __init__(self, difficulty):
        # needs a name
        self.reId()
        self.reName()
        self.exits = []
        self.entrances = []
        self.threats = []
        self.difficulty = difficulty
        self.alarm = getEncounter('alarm')
        self.lock = getEncounter('lock')
        self.theme = choice(['Fight','Social','Puzzle']) #this decides the types of threats
        #TODO inside of getEncounter lets add a dropoff thing so that the first is always guarenteed to be the type, then its a lesser chance on the next roll, and even less of a chance, and so on and so on, so that theres always a mix throughought the dungeon and not exclusively all the same stuff in each tile and hoping for generators to do mixes instead of having it be natural.
        #TODO This would disable the type in the summary probably? I dunno, I still kinda like the idea of the players getting that hint but its not really a thing thats dictated its a thing thats observed.
        #TODO maybe type should be inferred after the threats are rolled, thats not too difficutl to calculate. Just do some math with the threats and seeing which encounters they map to and go with the largest one.
        # probably also picks the type of alarm? Eh, that should be randomized
        # Same thing with lockboxes
        self.reTitle()

        self.countdown = randrange(4,12)


    def addExit(self, dungeonNode):
        self.exits.append(dungeonNode)

    def reId(self):
        self.id=''.join(sample(ascii_letters, k=8))
        # this might be better serviced by id(self) instead? https://docs.python.org/3/library/functions.html#id
        # Idk if it outputs something usable by mermaid though, but I don't know how important that is.
        pass

    def reName(self):
        self.name=haiku()
        pass

    def addEntrance(self, dungeonNode):
        self.entrances.append(dungeonNode)

    def getConnections(self) -> Set[DungeonNode]:
        return set(self.entrances + self.exits)

    def addGenerator(self):
        # generators double as signal nodes
        # each generator is also the key for the current difficulty
        self.generator = getEncounter('generator')
        self.reTitle()

    def clearGenerator(self):
        # generators double as signal nodes
        # each generator is also the key for the current difficulty
        del self.generator

    def addBenefit(self):
        # self.benefit = getEncounter('benefit') Maybe at some point it'll be this way but its easier to do it this way
        self.benefit = Encounters.benefit[floor(self.difficulty/len(Encounters.benefit))]
        self.reTitle()

    def clearBenefit(self):
        # generators double as signal nodes
        # each generator is also the key for the current difficulty
        del self.benefit

    def reTitle(self):
        badges = []
        if(hasattr(self, 'benefit')):
            badges.append('B')
        if(hasattr(self, 'generator')):
            badges.append('G')
        if(len(badges) > 0):
            badges = ''.join(badges)
            self.title=f'{self.id}({self.name} - {self.difficulty} - {badges})'
        else:
            self.title=f'{self.id}({self.name} - {self.difficulty})'

    # needs to be told its under the effects of a generator
    # this might turn into an element of the generator type
    # actually the dungeon builder cares about this

    def getThreatSummary(self):
        return ", ".join(self.threats)

    def getSummary(self):
        return f'{self.name} *(Level {self.difficulty} - {self.theme} - {self.getThreatSummary()})*'

    def getExitList(self):
        return list(map(lambda x: f'{self.title} --- {x.title}',self.exits))
    
class DungeonNodeBasic(DungeonNode):
    def __init__(self, difficulty):
        DungeonNode.__init__(self, difficulty)
        isBenefit = randrange(7) == 0
        for _ in range(difficulty):
            self.threats.append(getEncounter('threat'))
    

class DungeonNodeBoss(DungeonNode):
    ## bossNode
    # boss node needs to provide a theme
    # themes are just gonna be the element table types
    # 1 difficulty is allocated to the megavirus and the other difficutlies are allocated to hazards or viruses
    def __init__(self, difficulty):
        DungeonNode.__init__(self, difficulty)
        for _ in range(difficulty-1):
            self.threats.append(getEncounter('threat'))
        self.threats.append(getEncounter('boss'))
        pass

class DungeonNodeStarter(DungeonNode):
    def __init__(self):
        self.name='Start'
        self.title=self.name
        self.exits=[]
        self.entrances=[]
        self.threats=[]
