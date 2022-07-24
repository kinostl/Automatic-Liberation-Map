from LiberationMap import Dungeon
from EncounterConfig import EncounterConfig

dungeon = Dungeon(EncounterConfig({}), 7)
dungeon.printDiagram()
dungeon.printExpectedPlayTime()
dungeon.printEncounters()