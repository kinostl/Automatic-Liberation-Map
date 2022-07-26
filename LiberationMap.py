from __future__ import annotations
from typing import List
from random import randrange, choice
from math import floor
from itertools import chain, groupby
from LiberationMapTiles import DungeonNodeBasic, DungeonNodeBoss, DungeonNodeStarter, DungeonNode

class DungeonMap:
  def __init__(self):
    self.startingNode = DungeonNodeStarter()
    self.branches = []
  
  def getFlattenedBranches(self) -> List[DungeonNode]:
    difficulty = lambda x: x.difficulty
    return sorted(list(chain.from_iterable(self.branches)),key=difficulty)

  def getTotalDifficulty(self):
    return sum(map(lambda x: x.difficulty, self.getFlattenedBranches()))
  
  def _getDuplicates(self, key):
    duplicates=[]
    branches = self.getFlattenedBranches()
    for node in branches:
      isMatch = lambda x: getattr(x, key) == getattr(node, key)
      isNotSelf = lambda x: x != node
      isDuplicate = lambda x: isMatch(x) and isNotSelf(x)
      dupes = list(filter(isDuplicate, branches))
      duplicates.extend(dupes)
    return duplicates

  def _fixDuplicates(self):
    duplicateIds = self._getDuplicates('id')
    duplicateNames = self._getDuplicates('name')
    while(len(duplicateIds) > 0):
      for duplicate in duplicateIds:
        duplicate.reId()
      duplicateIds = self._getDuplicates('id')

    while(len(duplicateNames) > 0):
      for duplicate in duplicateNames:
        duplicate.reName()
      duplicateNames = self._getDuplicates('name')

  def append(self, nodes):
    self.startingNode.addExit(nodes[0])
    self.branches.append(nodes)
    self._fixDuplicates()
  
  def getExitList(self):
    return self.startingNode.getExitList()
  
  def nodesByDifficulty(self):
    difficulty = lambda x: x.difficulty
    return groupby(self.getFlattenedBranches(), key=difficulty)

class Dungeon:
  def __init__(self, playHours=4, timeScale=15):
    self.timeScale = timeScale
    totalPlayHours = playHours - (timeScale * 2) / 60
    totalDifficulty = (totalPlayHours * 60) / timeScale
    bossDifficulty = int(floor(((totalPlayHours / 4) * 60) / timeScale))
    self.maxDifficulty = bossDifficulty - 1
    if (self.maxDifficulty <= 0):
      raise Exception("Can not calculate parameters given, please change and try again.")
    if(playHours * timeScale > 105):
      # TODO It would be more fun if it went over the threshold it went into megadungeon mode and had multiple bosses or something.
      raise Exception("Time and Scale must total out to less than 105 minutes.")
    self.branches = DungeonMap()

    def connect(start, end):
      start.addExit(end)
      end.addEntrance(start) # we connect both to check for generators

    def getBranch(endingDifficulty):
      nodes = []
      for i in range(endingDifficulty):
        difficultyStep = i+1
        node = DungeonNodeBasic(difficultyStep)
        if(i > 0):
          connect(nodes[-1], node)
        nodes.append(node)
      return nodes

    def getBossBranch(endingDifficulty):
      nodes = getBranch(endingDifficulty - 1)
      node = DungeonNodeBoss(endingDifficulty)
      connect(nodes[-1], node)
      nodes.append(node)
      return nodes

    self.branches.append(getBossBranch(bossDifficulty))

    while (self.branches.getTotalDifficulty() < totalDifficulty):
      currentDifficulty = randrange(self.maxDifficulty)  + 1
      self.branches.append(getBranch(currentDifficulty))

    #add shortcuts
    def addShortcut(branch, start):
      endBranchDiff = choice([-1,1])
      endBranch = branch + endBranchDiff
      endDifficulty = start.difficulty + choice([0, 1])
      endDifficulty = endDifficulty - 1
      if(endBranch >= len(self.branches.branches)):
        endBranch = 0
      if (endDifficulty <= self.maxDifficulty):
        try:
          end = self.branches.branches[endBranch][endDifficulty]
          connect(start, end)
        except IndexError:
          pass

    for branch, nodes in enumerate(self.branches.branches):
      addShortcut(branch, nodes[-1])
      for node in nodes:
        shortcuts = randrange(3)
        for _ in range(shortcuts):
          addShortcut(branch, node)

    for _, nodes in self.branches.nodesByDifficulty():
      # TODO this is where I should put some of the code that makes generators modify stuff. The rest should be in the Bot Controls probably.
      choice(list(nodes)).addGenerator()

    for _, nodes in self.branches.nodesByDifficulty():
      # TODO this is where I should put some of the code that makes generators modify stuff. The rest should be in the Bot Controls probably.
      choice(list(nodes)).addBenefit()

  def printDiagram(self):
    print('flowchart TD')
    exits = self.branches.getExitList()
    for branch in self.branches.branches:
      for node in branch:
        exits+=node.getExitList()
    for exit in set(exits):
      print(f'\t{exit}')

  def printExpectedPlayTime(self):
    totalTime = 0
    for branch in self.branches.branches:
      for node in branch:
        totalTime = totalTime + (self.timeScale * node.difficulty)
    print(f'Expected Play Time: {totalTime/60}')
  
  # GM just gets a list of the Summaries. That seems way less intimidating. 
  # TODO This isn't very engaging, and should probably also list generators and network quirks and other inspirations
  # TODO Actually maybe the above should be a seperate printGmSummary tool?
  # TODO Does that mean there should be a printPlayerSummary tool as well? That could be a good of telling them what they've done to each square and where they still have to visit.
  # TODO Start off with a "GMs trust me every nope I don't like typing this, toggles it is default to fog of war"
  # TODO GM Command "show summary unfogged"
  # TODO GM Command "show summary unfogged to players"
  # TODO GM Command "unfog area"
  # TODO GM Command "Show more tiles?"
  # TODO Inform GM and Playes as necessary when something updates
  def printSummary(self):
    branches = self.branches.getFlattenedBranches()
    for node in branches:
      print(node.getSummary())

class DungeonBot(Dungeon):
  def printEncounters(self):
    def _getNumberAsEmoji(number):
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

    branches = self.branches.getFlattenedBranches()
    for node in branches:
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
        encounter.append(f'**{node.name}** *Level {node.difficulty} {node.theme}*')
        encounter.append('')
        encounter.append(f'**Countdown** {node.countdown}')
        encounter.append(f'**Alarm** {node.alarm} *( :x: to activate alarm.)*')
        encounter.append(f'**Lockbox** {node.lock} *( :white_check_mark:  to clear tile.)*')
        encounter.append('')
        encounter.append(f'**Threats** {node.getThreatSummary()} *(:boom: to delete contents.)*')
        if(hasattr(node, 'benefit')):
            encounter.append(f'**Benefit** {node.benefit} *(:ribbon: to collect benefit!)*')
        if(hasattr(node, 'generator')):
            encounter.append(f'**Generator** {node.generator} *( :wastebasket: to disable generator.)*')
        encounter.append('')
        encounter.append('**Exits *(Select to move.)***')
        for num, connection in enumerate(node.getConnections()):
            encounter.append(f'{_getNumberAsEmoji(num+1)} {connection.getSummary()}')
        print('\n'.join(encounter))

class DungeonWeb(Dungeon):
  def printEncounters(self):
    def _getNumberAsEmoji(number):
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

    branches = self.branches.getFlattenedBranches()
    for node in branches:
        encounter=[]
        encounter.append(f'**{node.name}** *Level {node.difficulty} {node.theme}*')
        encounter.append('')
        encounter.append(f'**Countdown** {node.countdown}')
        encounter.append(f'**Alarm** {node.alarm}')
        encounter.append(f'**Lockbox** {node.lock}')
        encounter.append('')
        encounter.append(f'**Threats** {node.getThreatSummary()}')
        if(hasattr(node, 'benefit')):
            encounter.append(f'**Benefit** {node.benefit} Mystery Data')
        if(hasattr(node, 'generator')):
            encounter.append(f'**Generator** {node.generator}')
        encounter.append('')
        encounter.append('**Exits**')
        for num, connection in enumerate(node.getConnections()):
            encounter.append(f'{_getNumberAsEmoji(num+1)} {connection.getSummary()}')
        print('\n'.join(encounter))