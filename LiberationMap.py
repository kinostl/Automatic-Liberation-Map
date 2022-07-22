from random import sample, randrange
from math import floor
from itertools import chain
from EncounterConfig import EncounterConfig
from LiberationMapTiles import DungeonNodeBasic, DungeonNodeBoss
from functools import reduce

class DungeonMap:
  def __init__(self):
    self.branches = []
  
  def getTotalDifficulty(self):
    return sum(map(lambda x: x.difficulty, chain.from_iterable(self.branches)))

  def append(self, node):
    self.branches.append(node)
  
  def getExitList(self):
    return map(lambda x: f'[*]-->{x[0].name}',self.branches)

class Dungeon:
  def __init__(self, playHours=4, timeScale=15):
    self.timeScale = timeScale
    totalPlayHours = playHours - (timeScale * 2) / 60
    totalDifficulty = (totalPlayHours * 60) / timeScale
    bossDifficulty = int(floor(((totalPlayHours / 4) * 60) / timeScale))
    maxDifficulty = bossDifficulty - 1
    if (maxDifficulty <= 0):
      raise Exception("Can not calculate parameters given, please change and try again.")
    self.branches = DungeonMap()
    self.encounterConfig = EncounterConfig({})

    def connect(start, end):
      start.addExit(end)
      end.addExit(start)

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
      currentDifficulty = randrange(maxDifficulty)  + 1
      self.branches.append(getBranch(currentDifficulty))

    #add shortcuts
    def addShortcut(i, start):
      endBranchDiff = sample([-1,1],1)[0]
      endBranch = i + endBranchDiff
      endDifficulty = start.difficulty + sample([0, 1],1)[0]
      if(endBranch >= len(self.branches.branches)):
        endBranch = endBranchDiff
      if (endDifficulty <= maxDifficulty) and (endDifficulty in self.branches.branches[endBranch]) and (start is not end):
        end = self.branches.branches[endBranch][endDifficulty]
        connect(start, end)

    for branch, nodes in enumerate(self.branches.branches):
      addShortcut(branch, nodes[-1])
      for node in nodes:
        shortcuts = randrange(3)
        for _ in range(shortcuts):
          addShortcut(branch, node)

  def printDiagram(self):
    print('stateDiagram-v2')
    for exit in self.branches.getExitList():
      print(f'\t{exit}')
    for branch in self.branches.branches:
      for node in branch:
        for exit in node.getExitList():
          print(f'\t{exit}')

  def printExpectedPlayTime(self):
    totalTime = 0
    for branch in self.branches.branches:
      for node in branch:
        totalTime = totalTime + (self.timeScale * node.difficulty)
    print(f'Expected Play Time: {totalTime/60}')