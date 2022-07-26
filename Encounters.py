from random import choice
import csv

themes = ['Nature', 'Fantasy', 'Science', 'Actions', 'Art', '???']
theme = choice(themes)
# this is a singleton so any time this is used elsewhere it'll be the same, which is nice.

with open("elementdata.tsv") as file:
    element = csv.DictReader(file, dialect=csv.excel_tab)
    element = [f'{x.get("element")} *(Hazard)*' for x in list(element) if x.get('category') == theme] # Im sorry this should be pandas but I am dedicated to not using pip while writing this
    # element = [x.get('element') for x in list(element)] # Im sorry this should be pandas but I am dedicated to not using pip while writing this

with open("virusdata.tsv") as file:
    # One day we'll need it like this but for now
    # virus = list(csv.DictReader(file, dialect=csv.excel_tab))
    virus = csv.DictReader(file, dialect=csv.excel_tab)
    virus = [f'{x.get("Name", "Mettaur")} *(Virus)*' for x in list(virus)][themes.index(theme) :: len(themes)] # Keeps it even and for some reason shuffle() and get the first len(elem) viruses just didn't appeal.
    # viruses are in order of type so this kinda striping probably should create somewhat consistent gameplay experiences in regards to always having a similar pool of virus types.

lock = [ 'Lockbox', 'CryptoLock', 'ProgLock', 'SyncLock', 'StealthLock' ]
threat = []
threat.extend(element)
threat.extend(virus)

# Okay this might be something to just do in getEncounter?
alarm = [
    f'Hazards! Spawns random element from the {theme} table. *(Its probably a good idea to base this off the difficulty level. Either roll an additional element for each difficulty level or increase how far it spreads or mention that its tougher than Normal. Maybe make it weaker if its a lower difficulty and it seems right. Such as making it Easy or single target.)*',
    'Backup! - Spawns random viruses. *(I would suggest doing this based on the difficulty level somehow. Like making the number of viruses equal to the difficulty. Either that or having them spawn on multiple tiles.)*',
    'High alert! All of the adjacent tiles have their Countdown reduced by the difficulty level. *(Tiles are adjacent if they share a connection. This mostly means the GM needs to check the chart.)*'
]

def getAlarm():
    # outcomes
    # This will be saved for another time when we're more focused on doing something super in depth using Progbot.

    return {
        'theme': 'theme',
        'style': 'style'
    }

generator = [ 'Amplifier', 'Spawner', 'Shaker', 'Scanner', 'Jammer' ]
benefit = ['Common', 'Uncommon', 'Rare']