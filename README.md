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

# Example Node

This is its own section because it is. This is what a node looks like. It contains a lot of information. Well, it looks something like this anyway. Anything thats obviously a filler word like `threat` or `alarm test` or `lock` is because the default getEncounter currently just returns the string its passed unless its alarm in which case it does a little logic for the getEncounters() function down the line. getEncounters() should probably be renamed to something more generic like getRoomDescription(). This is very muddy. Like MUD the software.

Its all very much output made for Progbot to interact with or any other bot that can receive emojis and spit out outputs somehow. This usually means Discord but I don't know what the future is. This might be more like a normal dictionary or something or left up to the implementer to decide what to do with but for right now I want this here instead of there. It might turn into a translation layer or something but thats over complicating something that very likely has a narrow usecase.

> **Misty Frost** *Level 2 fight*
>   
> **Countdown** 8  
> **Alarm** alarm test *( :x: to activate alarm.)*  
> **Lockbox** lock *( :white_check_mark:  to clear tile.)*  
>   
> **Threats** threat, threat *(:boom: to delete contents.)*  
>   
> **Exits *(Select to move.)***  
> :one: Fragrant Smoke *(Level 2 - fight - threat, threat)*  
> :two: Dry Meadow *(Level 1 - social - threat)*  
> :three: Spring Frost *(Level 3 - social - threat, threat)*

# Sources

Shoutout to this article for inspiring a lot of the code in this by writing and sharing [The Zelda Dungeon Generator:
Adopting Generative Grammars to
Create Levels for Action-Adventure
Games by Lavender](http://beckylavender.co.uk/wp-content/uploads/2017/11/ZDG_Dissertation.pdf). Specifically her study of Lenna's Inception in section 2.5.2
