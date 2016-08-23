**How is this going to work?**

So I think I need a plan of how I'm going to work this whole thing out. Once I've got this I can create the tests, as right now everything feels a bit directionless.

**Step 1 - Set Up of the game**

So to set up the game and visualise it I'm going to have python create 12 tables in SQLite3, as described below. In a nutshell the main table will be BoardTBL. This will contain all the information the board in the regular game contains.

After this 4 more tables will be created for the 2 main decks and their discard piles. 

Smaller tables for the event, epidemic and charater cards will also be created.

Each card will be given a unique random number from 1-72 which denotes it's position in either the player or infection deck, apart from charater cards, which will instead each get a unique random number from 1-4 depending on the number of players.

A table will also be set up with the number of cubes of each colour remaining to keep track of this.

Finally each player will have a table which gives the contents of their hand.

1- BoardTBL this contains: 
the name of each country 
the colour of each country
the number of connections it has
the names of the countries this country is connected to (each in it's own column, max of 6)
the number of cubes of each colour )each in it's own column, max of 5)
the number of research stations in the country

2 - pdTBL this contains:
	the name of the city card
	it's position in the deck

3 - pddTBL this contains:
	the name of the card

4 - idTBL this contains:
	the name of the infect city card
	it's position in the deck

5 - iddTBL this contains:
	the name of the infect city card

6 - edTBL this contains:
	the name of the event card
	it's position in the player deck

7 - cTBL this contains:
	the name of the card
	it's position in the charater deck

8 - cubesTBL this contains:
	the number of cubes of each colour left (5 columns)

9 - player1TBL this contains:
	the name of the card in the players hand

10 - player2TBL this contains:
	the name of the card in the players hand

11 - player3TBL this contains:
	the name of the card in the players hand

12 - player4TBL this contains:
	the name of the card in the players hand

13 - epTBL this contains:
	the name of the epidemic card
	it's position in the playerdeck

**Step 2 - Playing the game**

Not sure how to do this yet.

**Step 3 - Checking to see if the game has been won or lost**

Ditto on this. 
