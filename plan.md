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

There are 8 actions a player can complete in a turn, so I think defs to test each of these things is what is needed next

- Ferry / train to adjacent city
- direct flight discarding the card of the destination city
- charter flight discarding card from the departure city
- shuttle flight from one research station to another
- treat disease
- cure disease
- share knowledge
- build a research station 

**Step 3 - Checking to see if the game has been won or lost**

Ditto on this.

**Classes and Defs in PandemicGame.py**
***A- Class - startinggame***
1- startinglocals - Puts a research station in Atlanta, along with a given number of players.
2- BoardTBL - Sets up the gameboard from a given .txt file.
3- pdTBL - creates and populates the player deck
4- pddTBL - creates the player deck discard pile
5- idTBL - creates the infection deck
6- iddTBL - creates the infection deck discard pile
7- edTBL - shuffles the event cards together in a pile from a given .txt file.
8- cTBL - shuffles the character identity cards together in a pile from a given .txt file.
9- caTBL - gives all players an identity (no need to specify player numbers)
10 - cubesTBL - creates a table with stores the numbers of each time of cube not on the board.
11- shufpd - shuffles the player deck (with event cards) for a given number of players.
12- shufid - shuffles the infection deck.
13- player1TBL - draws a hand for player one for a given number of players.
14- player2TBL - draws a hand for player two for a given number of players.
15- player3TBL - draws a hand for player three for a given number of players.
16- player4TBL - draws a hand for player four for a given number of players.
17- epTBL - shuffles a given number of Epidemic cards into the player deck.
18- gsTBL - creates a game state table with the number of players, infection rate and outbreak count.
19- sginfect - infects 3 cities with 3 cubes, 3 with 2 and 3 with 1.
20- startnewgame - starts a new game for a given number of players, on a specific board, with a given number of epidemics using given event and character files.

***B - Class - inaturn***
1 - getplayer - returns the location of a given player. 
2 - getcityallcubes - returns all the cubes of any colour found in a given city.
3 - infectcities - infects cities at a given rate
4 - move - moves a given player from a given location to a given destination
5 - getxcube - returns the name of all cities with a given colour and given number of cubes in
6 - getoc - returns the current outbreak count 
7 - getir - returns the current infection rate
8 - gethand - returns the contents of a given players hand
9 - getcitycubes - returns the number of cubes of a given colour in a given city
10 - getcubes - returns the number of cubes remaining of a given colour
11 - usecube - reduces the remaining amount of a given colour of cube by 1.
12 - getidd - returns the cards in the infection deck discard pile
13 - getpdd - returns the cards in the player deck pile
14 - discard - for a given player discards a given card from their hand.

***C - Class - playeraction***
1 - mp - move a given player from a given location to another adjacent location, for an action.
2 - df - move a given player to given location dicarding the card of the destination city from their hand.
3 - cf - move a given player to a given location discarding the card of their current location from their hand.
4 - sf - move a given player from a given location to a given destination where there is a research station present at each locaton.
5 - td - remove 1 cube of a given colour from a given city, or all cubes of that colour if a cure has been discovered.
6 - cd - discard 5 given cards of the same colour to discover a cure for a disease.
7 - sk - moves a given card from a given player to another given player when both are in the same city and the city named on the card.
8 - br - a given player builds a research station in a given city discarding that city card if they are in the city on the card

