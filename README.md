
**What is this?**

This is a simple project I've started to help me learn how to use vim, python and github. When it's finished it should let somebody play the Pandemic board game as one or more of the players.

I'm about to start an OU degree in computing and IT and hoping for a career in IT eventually. The role I've got my eye on is one of full stack developer https://www.sitepoint.com/full-stack-developer/, although I understand this might already be old hat https://techcrunch.com/2014/11/08/the-rise-and-fall-of-the-full-stack-developer/. So I'm going to try to learn as much code as I can and focus on completing practical fun projects with other people alongside my course. 


**What am I trying to learn?**

I'd like to get my head round Python, SQL, and anything else relevant to make this work. I think that probably includes Git and how to use the command line in Linux (running Ubuntu at the moment). In the future I'd also like to learn

At least one kind of web server language, probably two (Apache, PHP I think)
At least one version of SQL
Some basic front end website languages (HTML, JavaScript and the like)


**What do the various files do / contain?**
There are 12 files in this repository:
1. fullboard.txt
2. game.py
3. pandemicgame.py
4. README.md
5. rules.md
6. testboard.txt
7. testcharacter.txt
8. testevent.txt
9. t_inaturn.py
10. t_makeboard.py
11. t_playeraction.py
12. t_game.py

**File 3 'pandemicgame.py'**
Written in python this file contains four different classes of def.

1: startinggame - This class contains all the defs which preform the actions needed to set up the game, although it does utilise actions  found in other classes.

2: inaturn - This class contains all the defs which carry out the most basic and simple actions that are completed in a turn, such as # moving a player or drawing a card.

3: playeraction - This class contains all the defs for the eight different player actions that can be completed in a turn. These are covered by nine different defs as sharing knowledge requires a def for giving a card and a def for taking a card.

4: game - This class contains all the defs which the players interact with to play the game. It should only require defs found in the playeraction class, and does not interact directly with the .db file which contains the game information.

**Classes and Defs in PandemicGame.py**
***Class One - startinggame***
This class contains all the defs which preform the actions needed to set up the game, although it does utilise actions found in other classes. It contains the following def's

1. BoardTBL (1 Argument)
Sets up the gameboard from a given .txt file (1st Argument). This has columns which give the name, colour, connections and cubes in a city. It also has columns which are set to 1 from 0 when a player or research station are present.

2. edTBL (1 Argument)
Shuffles the event cards together by giving each a random number from 0-500 in a column labled "pos". The cards used are taken from a given .txt file (1st Argument).

3. cubesTBL (0 Argument)
Creates a table with stores the numbers of each type of cube left to place on the board. This includes purple cubes, even though they are not used yet.

4. cTBL - (1 Argument) 
Shuffles the character identity cards together by giving each one a random number from 0-500 in a column labled "pos". The cards used are taken from a given .txt file (1st Argument).

5. caTBL - (0 Argument) 
Gives all players an identity (no need to specify player numbers).

6. idTBL - (0 Argument)
Creates the infection deck, using the info found in BoardTBL.

7. iddTBL - (0 Argument) 
Creates the infection deck discard pile.

8. shufid - (0 Argument)
Shuffles the infection deck cards together by giving each one a random number from 0-500 in a column labled "pos".

9. pdTBL - (0 Argument)
Creates and populates the player deck table with city cards for each city found in BoardTBL.

10. pddTBL - (0 Argument)
Creates the player deck discard pile.

11. shufpd - (1 Argument)
Shuffles the city cards and event cards together by giving each one a random number from 0-500 in a column labled "pos". These number of event cards used is based on the given number of players as an interger (1st Argument).

12. startinglocals - (1 Argument)
Updates the BoardTBL table with the basic starting game info. A research station is placed in Atlanta, and a number of players based on a given interger (1st Argument) are also placed there.

13. player1TBL - (1 Argument)
Draws a hand for player one for a game with a specific number of players based on a given interger (1st Argument) for the number of player 

14. player2TBL - (1 Argument)
Draws a hand for player two for a game with a specific number of players based on a given interger (1st Argument) for the number of player 

15. player3TBL - (1 Argument)
Draws a hand for player three for a game with a specific number of players based on a given interger (1st Argument) for the number of player 

16. player4TBL - (1 Argument)
Draws a hand for player four for a game with a specific number of players based on a given interger (1st Argument) for the number of player 

17. epTBL - (1 Argument)
Shuffles a given interger (1st Argument) of Epidemic cards into the player deck. 

The number of cards in the player deck currently are counted and is divided by the number of epidemic cards. This is then turned into a whole number rounded down called 'numberofcardsinapile' in the def.

The player cards are sorted into an by pos ascending, and the pos value of the Xth card where X = the number of cards in a pile x the number of epidemics already added. This pos value is then set as 'maxposnew'. A random number between 'maxposnew' and 'maxposold' (initally 0) is then given and assigned to the first epidemic card. 

The maxposnew value is then added to maxposold and the proccess is repeated until all the epidemics have been given a pos value and then added to the player deck.

18. gsTBL - (1 Argument)
Makes the game state table which includes:
The infection rate
The outbreak count
Number of players
Number of epidemics so far
The active player
The actions remaining in a turn.
The which diseases have been cured.

For a given interger (1st Argument) of players.


19. sginfect - (0 Argument)
This infects 3 cities with 3 cubes, 3 cities with 2 cubes and 3 cities with 1 cube. The used infection deck cards are placed in the infection deck discard pile.

This is done by infecting 9 cities as normal, then choosing 6 cities at random with at least 1 cube of any colour in. The first 3 of these cities have the cubes found there set to 2, and the next 3 have the number of cubes found set to 3.

To correct the number of cubes used the cities with 2 of cubes of each colour is then searched up, and set as a value for each colour, which by default is 0. A cube is then used X times where X is this value. This is then repeated for cities with 3 cubes in, but with 2 cubes used for X.

20. startnewgame - (5 Arguments)
Starts a new game for a given interger (1st Argument) of players, on a specific board given as a .txt file (2nd Argument). This game will use a given interger (3rd Argument) of epidemics and a given .txt file (4th Argument) for the event cards, and another .txt file (5th Argument) for the character cards. 

As the game is started each step is printed out, and after it has finished 'def start' from the game class is run to start the game.

21. startnewgameq (5 Arguments)
The same as startnewgame, but without the printing or running of 'def start' in the game class.

***Class Two - inaturn***
This class contains all the defs which preform the actions needed to set up the game, although it does utilise actions found in other classes. It contains the following def's

1. BoardTBL (1 Argument)


***B - Class - inaturn***
1 getplayer - returns the location of a given player. 
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
15 - pdraw - draws a single card for a given player, checking if it is an epidemic
16 - epidemic - carries out an epidemic on the board
17 - co - checks for unresolved outbreaks
18 - ic - infects a given city with a given colour
19 - action - reduces the current active players action by 1, and if zero moves to the next players turn
20 - rc - removes a cube of a given colour from a given location
21 - getap - returns the current active player

***C - Class - playeraction***
1 - trainboat - move a given player from a given location to another adjacent location, for an action.
2 - direct - move a given player to given location dicarding the card of the destination city from their hand.
3 - charter - move a given player to a given location discarding the card of their current location from their hand.
4 - shuttle - move a given player from a given location to a given destination where there is a research station present at each locaton.
5 - treat - remove 1 cube of a given colour from a given city, or all cubes of that colour if a cure has been discovered.
6 - cure - discard 5 given cards of the same colour to discover a cure for a disease.
7 - sk - moves a given card from a given player to another given player when both are in the same city and the city named on the card.
8 - br - a given player builds a research station in a given city discarding that city card if they are in the city on the card


