from LiberationMap import DungeonWeb
from random import choice

dungeon = DungeonWeb()
network = choice(['COM', 'ORG', 'NET', 'INT', 'EDU', 'GOV', 'MIL'])
name = dungeon.branches.getFlattenedBranches()[-1].name
output = [
    f'# {name}.{network}',
    dungeon.getExpectedPlayTime(),
    '',
    '```mermaid',
    dungeon.getDiagram(),
    '```',
    '',
    '---',
    '',
    dungeon.getSummary(),
    '',
    '---',
    '',
    dungeon.getEncounters()
]

output = "\n".join(output)
output = output.replace("\n", "  \n")

print(output)
