#!/home/minty/.pyenv/shims/python3
from random import sample, randrange
from math import floor

inputPlayHours = 4
timeThing = 15
totalPlayHours = inputPlayHours - (timeThing * 2) / 60
totalDifficulty = (totalPlayHours * 60) / timeThing
bossDifficulty = int(floor(((totalPlayHours / 4) * 60) / timeThing))
maxDifficulty = bossDifficulty - 1

remainingDifficulty = totalDifficulty - bossDifficulty

if (remainingDifficulty <= 0 or maxDifficulty <= 0):
  print("Something went wrong.")
  exit(1)

branches = []
nodes = []

for i in range(bossDifficulty):
  difficultyStep = i+1
  nodes.append(difficultyStep)
  remainingDifficulty = remainingDifficulty - difficultyStep

branches.append(nodes)
del nodes

while (remainingDifficulty > 0):

  currentDifficulty = randrange(maxDifficulty)  + 1
  nodes = []

  for i in range(currentDifficulty):
    difficultyStep = i+1
    nodes.append(difficultyStep)
    remainingDifficulty = remainingDifficulty - difficultyStep

  branches.append(nodes)


startingNodes = {}
diagramItems = []

print(branches)
for i, nodes in enumerate(branches):
  startingNodes[i]=[]

  startingNodes[i].append(nodes[-1])
  for node in nodes:
    shortcuts = randrange(3)
    for shortcut in range(shortcuts):
      startingNodes[i].append(node)
    if node - 1 == 0:
      diagramItems.append(f'[*]-->{i}.{node}')
    else:
      diagramItems.append(f'{i}.{node - 1}-->{i}.{node}')

for shortcuts in startingNodes.items():
  i = shortcuts[0]
  for node in shortcuts[1]:
    branchModifier = sample([-1,1],1)[0]
    difficultyModifier = sample([0, 1],1)[0]
    start = f'{i}.{node}'
    endBranch = i+branchModifier
    endDifficulty = node+difficultyModifier
    if (endBranch < 0):
      endBranch = len(branches) + endBranch
    if (endBranch >= len(branches)):
      endBranch = branchModifier

    end = f'{endBranch}.{endDifficulty}'

    if not (endDifficulty > maxDifficulty) and (endDifficulty in branches[endBranch]) and (start is not end):
      diagramItems.append(f'{start}-->{end}')

print('stateDiagram-v2')
for item in set(diagramItems):
  print(f'\t{item}')

totalTime = 0
for branch in branches:
  for node in branch:
    totalTime = totalTime + (timeThing * node)

print(f'Expected Play Time: {totalTime/60}')