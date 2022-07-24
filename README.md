# Automatic Liberation Map

The goal of this project is to provide a class that can produce strings that Progbot can print out to run an almost automated liberation map. The strings it produces are vague prompts that are strong enough to do most of the decision making for the game master and give them inspiration for their own descriptions.

# Coding Style

I don't want to deal with pip for whats essentially a library, so I'm trying to keep everything batteries included for python 3.8, if you're contributing I'd appreciate that being respected, but I'll understand if the scope changes from there. I'll probably be approaching code reviews with that in mind

# What this does not do

This is going to handle some amount of memory, like fog of war and cleared tiles, but all the controls will be handled by Progbot or as another file inside this to act as glue. So things should be designed with that in mind. It'd be nice to be able to reuse this for other projects as wanted, the concepts in here are very globally applied and the EncounterConfig file gives a lot of flexibility to that. Future versions should probably remove the need to fork this to use it, that'd be nice.
