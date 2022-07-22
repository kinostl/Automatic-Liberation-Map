from LiberationMap import Dungeon
from EncounterConfig import EncounterConfig

dungeon = Dungeon(EncounterConfig({}))
dungeon.printDiagram()
dungeon.printExpectedPlayTime()