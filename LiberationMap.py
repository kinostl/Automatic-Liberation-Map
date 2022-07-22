from random import sample, randrange
from math import floor
from itertools import chain
from EncounterConfig import EncounterConfig
from LiberationMapTiles import DungeonNodeBasic, DungeonNodeBoss, DungeonNodeStarter

class DungeonMap:
  def __init__(self):
    self.startingNode = DungeonNodeStarter()
    self.branches = []
  
  def getTotalDifficulty(self):
    return sum(map(lambda x: x.difficulty, chain.from_iterable(self.branches)))

  def append(self, nodes):
    self.startingNode.addExit(nodes[0])
    self.branches.append(nodes)
  
  def getExitList(self):
    return self.startingNode.getExitList()

class Dungeon:
  def __init__(self, playHours=4, timeScale=15):
    self.timeScale = timeScale
    totalPlayHours = playHours - (timeScale * 2) / 60
    totalDifficulty = (totalPlayHours * 60) / timeScale
    bossDifficulty = int(floor(((totalPlayHours / 4) * 60) / timeScale))
    self.maxDifficulty = bossDifficulty - 1
    if (self.maxDifficulty <= 0):
      raise Exception("Can not calculate parameters given, please change and try again.")
    self.branches = DungeonMap()
    self.encounterConfig = EncounterConfig({})

    def connect(start, end):
      start.addExit(end)
      # end.addExit(start)

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
      endBranchDiff = sample([-1,1],1)[0]
      endBranch = branch + endBranchDiff
      endDifficulty = start.difficulty + sample([0, 1],1)[0]
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