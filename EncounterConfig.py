from random import choice
import Encounters

# This should be custom implemented by whoever is using this thing if they bother to fork. 
def getEncounter(type):
    return choice(getattr(Encounters, type, type))