from random import randrange, choice
from math import floor
from itertools import chain, groupby
from LiberationMapTiles import DungeonNodeBasic, DungeonNodeBoss, DungeonNodeStarter
import sys

class DungeonMap:
  def __init__(self):
    self.startingNode = DungeonNodeStarter()
    self.branches = []
  
  def getFlattenedBranches(self):
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
  def __init__(self, encounterConfig, playHours=4, timeScale=15):
    self.timeScale = timeScale
    totalPlayHours = playHours - (timeScale * 2) / 60
    totalDifficulty = (totalPlayHours * 60) / timeScale
    bossDifficulty = int(floor(((totalPlayHours / 4) * 60) / timeScale))
    self.maxDifficulty = bossDifficulty - 1
    if (self.maxDifficulty <= 0):
      raise Exception("Can not calculate parameters given, please change and try again.")
    self.branches = DungeonMap()
    self.encounterConfig = encounterConfig

    def connect(start, end):
      start.addExit(end)
      end.addEntrance(start) # we connect both to check for generators

    def getBranch(endingDifficulty):
      nodes = []
      for i in range(endingDifficulty):
        difficultyStep = i+1
        node = DungeonNodeBasic(self.encounterConfig, difficultyStep, '?')
        if(i > 0):
          connect(nodes[-1], node)
        nodes.append(node)
      return nodes

    def getBossBranch(endingDifficulty):
      nodes = getBranch(endingDifficulty - 1)
      node = DungeonNodeBoss(self.encounterConfig, endingDifficulty, '?')
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
      choice(list(nodes)).addGenerator()

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