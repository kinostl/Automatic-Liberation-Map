from __future__ import annotations
from typing import Set
from random import randrange, sample, choice
from RandomName import haiku
from string import ascii_letters
from EncounterConfig import getEncounter

class DungeonNode:
    # will be provided a difficulty
    # will be provided a theme
    # This should probably be taking an EncounterConfig object or something so that I can have things be loaded in
    def __init__(self, difficulty):
        # needs a name
        self.reId()
        self.reName()
        self.encounter = []
        self.exits = []
        self.entrances = []
        self.threats = []
        self.difficulty = difficulty
        self.alarm = getEncounter('alarm')
        self.lock = getEncounter('lock')
        self.theme = choice(['fight','social','puzzle']) #this decides the types of threats
        #TODO inside of getEncounter lets add a dropoff thing so that the first is always guarenteed to be the type, then its a lesser chance on the next roll, and even less of a chance, and so on and so on, so that theres always a mix throughought the dungeon and not exclusively all the same stuff in each tile and hoping for generators to do mixes instead of having it be natural.
        #TODO This would disable the type in the summary probably? I dunno, I still kinda like the idea of the players getting that hint but its not really a thing thats dictated its a thing thats observed.
        #TODO maybe type should be inferred after the threats are rolled, thats not too difficutl to calculate. Just do some math with the threats and seeing which encounters they map to and go with the largest one.
        # probably also picks the type of alarm? Eh, that should be randomized
        # Same thing with lockboxes
        self.title=f'{self.id}({self.name} - {self.difficulty})'

        self.countdown = randrange(4,12)


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

    def getConnections(self) -> Set[DungeonNode]:
        return set(self.entrances + self.exits)

    def addGenerator(self):
        # generators double as signal nodes
        # each generator is also the key for the current difficulty
        self.generator = getEncounter('generator')
        self.title=f'{self.id}({self.name} - {self.difficulty} - Generator)'

    def clearGenerator(self):
        # generators double as signal nodes
        # each generator is also the key for the current difficulty
        del self.generator

    # needs to be told its under the effects of a generator
    # this might turn into an element of the generator type
    # actually the dungeon builder cares about this

    def getThreatSummary(self):
        return ", ".join(self.threats)
    def getSummary(self):
        return f'{self.name} *(Level {self.difficulty} - {self.theme} - {self.getThreatSummary()})*'

    def getExitList(self):
        return list(map(lambda x: f'{self.title} --- {x.title}',self.exits))
    
    def _getNumberAsEmoji(self, number):
        numberEmoji = {
            '1':':one:',
            '2':':two:',
            '3':':three:',
            '4':':four:',
            '5':':five:',
            '6':':six:',
            '7':':seven:',
            '8':':eight:',
            '9':':nine:',
            '0':':zero:',
        }
        numberString = ''.join(map(lambda x: numberEmoji[x], list(str(number))))
        return numberString


    def getEncounters(self):
        # TODO This should make a list of the encounters, the exits, the theme, the name. Exits should all have a Number Emoji next to them. (Consideration - Maybe DungeonNodes should get a random emoji that is then referenced here instead of numbers?)
        # Also it lists any hazards or viruses and the like

        # **Flying Villa *Level 2 Puzzle***

        # **Countdown** 4
        # **Alarm** Politics Hazard *( :x: to activate alarm.)*
        # **Lockbox** Cryptolock *( :white_check_mark:  to clear tile.)*

        # **Threats** Candy, Doors, Mettaur *(:boom: to delete contents.)*
        # **Generator** Spawner *( :wastebasket: to disable generator.)*

        # **Exits (Select to move.)**
        # :one: Summer Glitter *(Level 1 Fight - Ninjoy)*
        # :two: Quiet Sun *(Level 2 Puzzle - Blocks, Balloons)*

        encounter=[]
        encounter.append(f'**{self.name}** *Level {self.difficulty} {self.theme}*')
        encounter.append('')
        encounter.append(f'**Countdown** {self.countdown}')
        encounter.append(f'**Alarm** {self.alarm.get("theme")} {self.alarm.get("style")} *( :x: to activate alarm.)*')
        encounter.append(f'**Lockbox** {self.lock} *( :white_check_mark:  to clear tile.)*')
        encounter.append('')
        encounter.append(f'**Threats** {self.getThreatSummary()} *(:boom: to delete contents.)*')
        if(hasattr(self, 'generator')):
            encounter.append(f'**Generator** {self.generator} *( :wastebasket: to disable generator.)*')
        encounter.append('')
        encounter.append('**Exits *(Select to move.)***')
        for num, connection in enumerate(self.getConnections()):
            encounter.append(f'{self._getNumberAsEmoji(num+1)} {connection.getSummary()}')
        return '\n'.join(encounter)
        # TODO Most of these variables aren't real also threats probably needs to be a function or something cause its probably a list that needs to be turned into a string.

class DungeonNodeBasic(DungeonNode):
    def __init__(self, difficulty):
        DungeonNode.__init__(self, difficulty)
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
        self.encounter.append('boss')
        pass

class DungeonNodeStarter(DungeonNode):
    def __init__(self):
        self.name='Start'
        self.title=self.name
        self.exits=[]
        self.entrances=[]
        self.threats=[]