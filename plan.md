**How is this going to work?**

So I think I need a plan of how I'm going to work this whole thing out. Once I've got this I can create the tests, as right now everything feels a bit directionless.

**Step 1 - Set Up of the game**

At the end of set up 4 tables should exist (5 if the discard for tables 2 and 3 are included)

1 - boardTBL with all the board information (cubes on cities, location of players, locations of research stations)
2 - shufpd with all the cards left in the player deck after hands have been drawn
3 - pdd, the discard pile of the player deck
4 - shufid with all the cards in the infection deck, after cities have been infected
5 - idd, the discard pile of the infection deck
6 - game state table which contains the infection rate and number of outbreaks

tables should also exist for each player, giving them the cards in their hands.

**Step 2 - Playing the game**

Not sure how to do this yet. My first guess is that commands on how to understand what the board looks like would be great. While an ASCII visualisation would be nice, some simple commands like "find out number of red cubes left" and whatnot are probably a good idea to come up with. Below is a list of the needed base commands

- How many cubes in city X
- Location of player X
- Cards in idd
- Cards in pdd
- Cards in player X hand
- Cubes of colour X remaining
- Infection rate
- Number of outbreaks

Def's to find out these things are probably the most important thing to code.

**Step 3 - Checking to see if the game has been won or lost**

Ditto on this. 
