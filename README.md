# Automatic Liberation Map

The goal of this project is to provide a class that can produce strings that Progbot can print out to run an almost automated liberation map. The strings it produces are vague prompts that are strong enough to do most of the decision making for the game master and give them inspiration for their own descriptions.

# Coding Style

I don't want to deal with pip for whats essentially a library, so I'm trying to keep everything batteries included for python 3.8, if you're contributing I'd appreciate that being respected, but I'll understand if the scope changes from there. I'll probably be approaching code reviews with that in mind

# What this does not do

This is going to handle some amount of memory, like fog of war and cleared tiles, but all the controls will be handled by Progbot or as another file inside this to act as glue. So things should be designed with that in mind. It'd be nice to be able to reuse this for other projects as wanted, the concepts in here are very globally applied and the EncounterConfig file gives a lot of flexibility to that. Future versions should probably remove the need to fork this to use it, that'd be nice.

# Example Outputs

This is what you get literally if you run it.

```
flowchart TD
	jAZVyMQo(little flower - 1) --- oiBINLWc(wild wind - 2)
	zsiIKJpf(white sun - 1) --- rboFBegQ(muddy glitter - 2)
	gwzNIcxp(old lake - 1) --- oiBINLWc(wild wind - 2)
	jAZVyMQo(little flower - 1) --- jEJNfQOG(falling morning - 2 - Generator)
	oSuztwaK(holy resonance - 1 - Generator) --- jEJNfQOG(falling morning - 2 - Generator)
	Start --- DFmjauPT(silent meadow - 1)
	Start --- zsiIKJpf(white sun - 1)
	jEJNfQOG(falling morning - 2 - Generator) --- rboFBegQ(muddy glitter - 2)
	oiBINLWc(wild wind - 2) --- zsDgyiOr(silent grass - 3 - Generator)
	Start --- gwzNIcxp(old lake - 1)
	Start --- oSuztwaK(holy resonance - 1 - Generator)
	jAZVyMQo(little flower - 1) --- gwzNIcxp(old lake - 1)
	oSuztwaK(holy resonance - 1 - Generator) --- zsiIKJpf(white sun - 1)
	DFmjauPT(silent meadow - 1) --- gwzNIcxp(old lake - 1)
	Start --- jAZVyMQo(little flower - 1)
	DFmjauPT(silent meadow - 1) --- rboFBegQ(muddy glitter - 2)
---
Expected Play Time: 3.5
---
old lake *(Level 1 - ? - threat)*
little flower *(Level 1 - ? - threat)*
holy resonance *(Level 1 - ? - threat)*
white sun *(Level 1 - ? - threat)*
silent meadow *(Level 1 - ? - threat)*
wild wind *(Level 2 - ? - threat,threat)*
falling morning *(Level 2 - ? - threat,threat)*
muddy glitter *(Level 2 - ? - threat,threat)*
silent grass *(Level 3 - ? - threat,threat)*
```

Threat will be less generic things like `fire` or `mettaur` representing viruses or hazards or the like. The `?` represents why type of tile it is, and might be removed at some point, since the collection of threats is more versatile than the guidance of what the tile type is. A player can't move to the next level until they've deleted the generator/signal node of their current level. 

The final node of every one of these maps spends one of its threats on a megavirus. This might travel based on the type it is, but this is up to the GM to do.

This is the type of dungeon it creates. The players probably won't be presented this, this is just for documentation purposes. The game master might receive it.

```mermaid
flowchart TD
	jAZVyMQo(little flower - 1) --- oiBINLWc(wild wind - 2)
	zsiIKJpf(white sun - 1) --- rboFBegQ(muddy glitter - 2)
	gwzNIcxp(old lake - 1) --- oiBINLWc(wild wind - 2)
	jAZVyMQo(little flower - 1) --- jEJNfQOG(falling morning - 2 - Generator)
	oSuztwaK(holy resonance - 1 - Generator) --- jEJNfQOG(falling morning - 2 - Generator)
	Start --- DFmjauPT(silent meadow - 1)
	Start --- zsiIKJpf(white sun - 1)
	jEJNfQOG(falling morning - 2 - Generator) --- rboFBegQ(muddy glitter - 2)
	oiBINLWc(wild wind - 2) --- zsDgyiOr(silent grass - 3 - Generator)
	Start --- gwzNIcxp(old lake - 1)
	Start --- oSuztwaK(holy resonance - 1 - Generator)
	jAZVyMQo(little flower - 1) --- gwzNIcxp(old lake - 1)
	oSuztwaK(holy resonance - 1 - Generator) --- zsiIKJpf(white sun - 1)
	DFmjauPT(silent meadow - 1) --- gwzNIcxp(old lake - 1)
	Start --- jAZVyMQo(little flower - 1)
	DFmjauPT(silent meadow - 1) --- rboFBegQ(muddy glitter - 2)
  ```
