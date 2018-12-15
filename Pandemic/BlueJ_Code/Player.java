
/**
 * Write a description of class Player here.
 * 
 * @author (Joe Salmon) 
 * @version (03.12.2018)
 */
import java.util.Random;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Collections;
public class Player

{

    String playerName;
    int tactic;
    GameBoard pandemicBoard;
    int playerAction;
    boolean activePlayer;
    PlayerCard[] hand;
    Piece playerPiece;
    String[] possibleColour = {"red","blue","yellow","black","purple"};
    City[] travelMap;


    /**
     * Constructor for objects of class Player
     */
    public Player(String givenName)
    {
        playerName = givenName;
        hand = new PlayerCard[0];
        playerAction = 4;
        tactic = 50;
    }
    
    public void setGameBoard(GameBoard currentBoard)
    {
        pandemicBoard = currentBoard;
    }
    
    
    
    public void drawCard(int numberOfCards)
    {
        // draws a card for the player in question from the board they are sat at
        for (int i = 0; i<numberOfCards; i++)
        {
            if (pandemicBoard.playerDeck.getSize()!= 0)
            {
                addCard(pandemicBoard.playerDeck.drawTop(this));
                System.out.println(this.getPlayerName() + " draws a card");
            }
            else 
            {
                System.out.println("no more cards left");
            }
        }
    }
    
    public void setPlayerPiece(Piece newPiece)
    {
        playerPiece = newPiece;
    }

    // adds a new card to the players hand.
    public void addCard(PlayerCard addedCard)
    {
        if (addedCard.isEpidemic)
        {
            System.out.println("EPIDEMIC DRAWN!");
            pandemicBoard.resolveEpidemic();
        }
        else
        {
            PlayerCard[] newHand = new PlayerCard[hand.length+1];
            int i = hand.length;
            while (i > 0)
            {
                newHand[i]= hand[i-1];
                i = i-1;
            }
            newHand[0]=addedCard;
            hand = newHand;
        }
    }
    
    public int getCountXCards(String colour)
    {
        int toReturn = 0;
        for (int i = 0 ; i < hand.length; i++)
        {
            if (hand[i].getCardColour().equals(colour))
            {
                toReturn ++;
            }
        }
        return toReturn;
    }    
    
    public int getPlayerAction()
    {
        return playerAction;
    }
    
    public void decrementPlayerAction()
    {
        playerAction--;
    }
    
    // sets a players action back to 4
    public void resetPlayerAction()
    {
        playerAction=4;
    }
    
    public String getPlayerName()
    {
        return playerName;
    }
    
    // Returns an array with the players cards in hand
    public PlayerCard[] getHand()
    {
        return hand;
    }
    
    /**
     * These are the methods used to make player actions happen.
     */
    public boolean checkDestinationConnected (City location, City destination)
    {
        int numberConnections = location.getConnectedCities().length;
        for (int i = 0; i < numberConnections; i++)
        {
            if (destination == (location.getConnectedCities()[i]))
            {
//                System.out.println("found a match");
                return true;
            }
            else
            {
//                System.out.println("not connected city");
                
            }
        }
        return false;
    }
    
    // checks a player has a card, and returns its position in the array.
    public int checkPlayerCard(String cardName)
    {
        int numberCardsInHand = getHand().length;
        for (int i = 0; i < numberCardsInHand; i++)
        {
            if (cardName.equals(getHand()[i].getCardName()))
                {
//                    System.out.println("found matching card in hand");
                    return i;
                }
            else
                {
//                    System.out.println("not found yet");
                }
        }
        return 0;
    }
    
    /**
     * sets a card in hand to null, then calls methods to put it in the discard pile
     * and remove the null values from the hand.
     */ 
    public void discardCard(String cardName)
    {
        int toDiscard = checkPlayerCard(cardName);
        pandemicBoard.addPlayerCardDiscard(hand[toDiscard]);
        hand[toDiscard] = null;
        hand = removeNulls(hand);

    }


    public void discardCureCards(String colour)
    {
        int numberToDiscard = pandemicBoard.getNeededForCure();
        for (int i = 0 ; i < numberToDiscard ; i ++)
        {
            for (int x = 0 ; x < hand.length ; x++ )
            {
                if (hand[x].getCardColour().equals(colour))
                {
                    discardCard(hand[x].getCardName());
                    break;
                }
            }
        }
    }

    

    public PlayerCard[] removeNulls(PlayerCard[] playerCardArray)
    {
        PlayerCard[] firstArray = playerCardArray;
        List<PlayerCard> list = new ArrayList<PlayerCard>();
        for(PlayerCard k : firstArray )
        {
            if(k != null)
            {
                list.add(k);
            }
        }
        firstArray = list.toArray(new PlayerCard[list.size()]);
        return firstArray;
    }
    
    // checks the cure can be discovered by the player.
    public boolean checkDiscoverCure(City location, String diseaseColour)
    {
        if (pandemicBoard.checkResearchStation(location) && 
        getCountXCards(diseaseColour) >= pandemicBoard.getNeededForCure())
        {
            System.out.println("Its possible to discover a cure");
            return true;
        }
        return false;
    }
    
    // Checks the city the player is try to treat disease in is where they are and 
    // has cubes in it of that colour.
    public boolean checkTreatDisease(City location, String colour)
    {
        boolean toReturn = true;
        if (location == playerPiece.getLocation())
        {
            // System.out.println("In the right place");
        }
        else
        {
            System.out.println("not in the right place");
            toReturn = false;
        }
        if (location.getCubeColour(colour)>0)
        {
            // System.out.println("There are some cubes of that colour");
        }
        else
        {
            System.out.println("No cubes of that colour");
            toReturn = false;
        }
        return toReturn;        
    }
    
    public boolean checkLocationCard ()
    {
        boolean toReturn = false;
        String locationName = playerPiece.getLocation().getName();
        for (int i = 0 ; i < hand.length ; i ++)
        {
            // System.out.println("Looking at " + locationName + " and " + hand[i].getName());
            if (locationName == hand[i].getName())
            {
                System.out.println("and have the card.");
                toReturn = true;
            }
        }
        return toReturn;
    }
    
    
    
    
    /**
     *These are the main methods used to control the players actions
     */
    
    //Build research station
    public boolean buildResearchStation (City location)
    {
        String locationName = location.getName();
        if (checkLocationCard() && 
        !pandemicBoard.checkResearchStation(location) && 
        pandemicBoard.checkResearchStation(pandemicBoard.unplaced))
        {
            discardCard(locationName);
            pandemicBoard.setUnplacedResearch(location);
            decrementPlayerAction();
            // System.out.println("building a research station in " + locationName);
            return true;
        }
        return false;
    }
    
    // Treat disease action
    public boolean treatDisease (City location, String colour)
    {
        if(checkTreatDisease(location,colour))
        {
            System.out.println("Removing a " + colour + " cube from " + location.getName());
            location.removeCube(colour);
            decrementPlayerAction();
            return true;
        }
        return false;
    }
    
    
    
    // Drive action
    public boolean driveCity (City location, City destination)
    {
        // System.out.println("attempting to move " + getPlayerName() + " to " + destination.getName() + " from "+ location.getName());
        if (checkDestinationConnected(location,destination))
        {
            System.out.println(getPlayerName() + " drives from " + location.getName() + " to " + destination.getName() + ".");
            playerPiece.setLocation(destination);
            decrementPlayerAction();
            return true;
        }
        else 
        {
            System.out.println("the location isn't connected");
        }
        return false;
    }
    
    // Charter Flight action
    public boolean charterFlight(City location, City destination)
    {
//        System.out.println(getPlayerName() + " wants to flying from " + 
//        location.getName() + " to "+ destination.getName() + 
//        " on a charter flight");
        if (checkPlayerCard(location.getName())>0)
        {
            System.out.println(getPlayerName() + "takes a charter flight to " + 
            destination.getName() + " from " + location.getName() );
            discardCard(location.getName());
            playerPiece.setLocation(destination);
            decrementPlayerAction();
            return true;
        }
        return false;
    }
    
    // Discover Cure action
    public boolean discoverCure(City location, String colour)
    {
        if (checkDiscoverCure(location,colour) && 
        playerPiece.getLocation().equals(location))
        {
            discardCureCards(colour);
            pandemicBoard.cureDisease(colour);
            decrementPlayerAction();
            return true;
        }
        return false;    
    }
    
    
    /**
     * These methods are used for AI controlled players
     */
    public void makeDecision()
    {
        System.out.print(this.getPlayerName() + " is thinking..... ");
        boolean checkCure = checkCureWorthIt();
        if (checkCure)
        {
            System.out.println("might be worth trying to find a cure.");
            checkTryCure();
        }
        if (!checkCure && (getDistanceResearch() > 3) && (tactic > 0) )
        {
            tactic--;
            System.out.print("They are far enough from a research station to consider building one.");
            if (!buildResearchStation(playerPiece.getLocation()))
            {
                System.out.println(" Can't find the required card.");
                fireFight();
            }
        }
        else if (!checkCure)
        {
            fireFight();
            fireFight();
            fireFight();
            fireFight();
            tactic--;
        }
        
        if (tactic < -500 )
        {
            System.out.println("out of ideas, will drive randomly");
            driveRandom();
        }
        tactic--;
    }
    
    // Player will either treat disease or go to a city with 3 cubes.
    public void fireFight()
    {
            System.out.print("Wants to treat disease... ");
            if (!tryTreat(3))
            {
                if (!go3CubeCities())
                {
                    tryTreat(2);
                    if (!go2CubeCities())
                    {
                        tryTreat(1);
                        if (!go1CubeCities())
                        {
                            System.out.println("Going to drive randomly as can't think of anything.");
                            driveRandom();
                        }
                    }
                }
            }                
    }
    
    // Check to see if the disease can be cured if threshold of cubes is met.
    public boolean tryTreat(int threshold)
    {
        boolean toReturn = false;

        City locationCity = playerPiece.getLocation();
        if (locationCity.getMaxCube() >= threshold)
        {
            System.out.println("As there are " + threshold + " cubes in " + locationCity.getName() + " " + this.getPlayerName() + " will try and treat disease.");
            String locationColour = locationCity.getColour();
            treatDisease(locationCity,locationColour);
            toReturn = true;
        }
        else 
        {
            System.out.println("Doesn't think it's worth trying to treat here.");
        }
        return toReturn;
        
    }
    
    public boolean checkTryCure()
    {
        if (checkCureWorthIt())
        {
            if (discoverCure(playerPiece.getLocation(),tryCureCardColour()))
            {
                System.out.println(this.getPlayerName() + "has discovered a cure!");
                for (int i = 0 ; i < 5 ; i ++)
                {
                    System.out.println("WHOOO!");
                }
                return true;
            }
            else
            {
                System.out.println("They need to go to a researh station.");
                tryDriveResearch();
            }
        }
        else 
        {
                // System.out.println("no point in trying to find a cure.");
        }
        return false;
    }
    
    public void tryDriveResearch()
    {
        System.out.println("Setting cities with research stations as destinations.");
        getDistances(pandemicBoard.getResearchLocations());
        // System.out.println("Calculating destination");
        City toDriveTo = calculateDestination();
        // System.out.println("I'll try to drive to " + toDriveTo.getName());
        driveCity(playerPiece.getLocation(),toDriveTo);        
    }
    

    
    
    
    public boolean checkCureWorthIt()
    {
        String toCure = tryCureCardColour();
        if (toCure != null)
        {
            for (int i = 0 ; i < pandemicBoard.diseases.length ; i ++)
            {
                Disease disease = pandemicBoard.diseases[i];
                if (toCure == disease.getColour() && !disease.getCured())
                {
                    return true;
                }
            }
            
        }
        return false;
        
        
    }
    
    
    /** 
    * Check to see if the count of cards in any colour equal the number required
    * for a cure
    */
        
    public String tryCureCardColour()
    {
        for (int i = 0; i < pandemicBoard.getNumberColours(); i ++)
        {
            if (getCountXCards(possibleColour[i]) >= pandemicBoard.getNeededForCure())
            {
                return possibleColour[i];
            }           
        }
        return null;
    }
    
    public int getDistanceResearch()
    {
        getDistances(pandemicBoard.getResearchLocations());
        return playerPiece.getLocation().getDistance();
    }
    
    
    public void getDistances(City[] destinations)
    {
        pandemicBoard.resetDistances();
        setDestination(destinations);
        int distance = 1;
        while (playerPiece.getLocation().getDistance() == 9999999)
        {
            // System.out.println("Looking for places distance of " + distance);
            for (int i = 0 ; i < pandemicBoard.cities.length ; i ++)
            {
                for (int x = 0 ; x < 6 ; x ++)
                {
                    if (pandemicBoard.cities[i].getDistance() == (distance-1) 
                    && pandemicBoard.cities[i].getConnectedCities()[x].getDistance() > distance)
                    {
                        pandemicBoard.cities[i].getConnectedCities()[x].setDistance(distance);
                    }
                }

            }
            distance ++;
        }
        
    }
    
    public void setDestination(City[] destinations)
    {
        for (int i = 0 ; i < destinations.length ; i ++)
        {
            destinations[i].setDistance(0);
        }        
    }
    
    
    
    
    // Try to charter a flight to a random city
    public void charterRandom()
    {
        Random rand = new Random();
        int n = rand.nextInt(pandemicBoard.cities.length);
        charterFlight(playerPiece.getLocation(),pandemicBoard.cities[n]);
           
    }
    
    
    // try to drive to random city until a possible city is chosen.
    public void driveRandom()
    {
        boolean foundDestination = false;
        while (foundDestination == false)
        {
            Random rand = new Random();
            int n = rand.nextInt(playerPiece.getLocationConnections().length);
            if (playerPiece.getLocationConnections()[n].getName().equals(" "))
            {
                // System.out.println("can't do that!");
            }
            else 
            {
                foundDestination = driveCity(playerPiece.getLocation(),playerPiece.getLocationConnections()[n]);
            }
                
                
                
        }
    }
    
    public City calculateDestination()
    {
        int closestDestination = 9999999;
        City toReturn = new City("error!","error!");
        for (int i = 0 ; i < playerPiece.getLocationConnections().length; i++)
        {
            if (!playerPiece.getLocationConnections()[i].getName().equals(" "))
            {
                //System.out.print("might go to " + playerPiece.getLocationConnections()[i].getName());
                //System.out.println(" which has a distance of " + playerPiece.getLocationConnections()[i].getDistance());
            }
            if (playerPiece.getLocationConnections()[i].getDistance() < closestDestination &&
            !playerPiece.getLocationConnections()[i].getName().equals(" "))
            {
                //System.out.println("Will probably go to " + playerPiece.getLocationConnections()[i].getName());
                toReturn = playerPiece.getLocationConnections()[i];
                closestDestination = playerPiece.getLocationConnections()[i].getDistance();
            }
            
        }
        return toReturn;
    }
    
    public boolean go3CubeCities()
    {        
        City[] cube3Cities = pandemicBoard.get3CubeCities();
        if (cube3Cities.length > 0)
        {
            //System.out.print("Setting 3 cube cities -");
            for (int i = 0 ; i < cube3Cities.length ; i ++)
            {
                //System.out.print(" " + cube3Cities[i].getName());
            }
            getDistances(cube3Cities);
            //System.out.println(" as destinations.");
            City toDriveTo = calculateDestination();
            //System.out.println(this.getPlayerName() + " will go to " + toDriveTo.getName());
            driveCity(playerPiece.getLocation(),toDriveTo);
            return true;
        }
        else
        {
            System.out.println("No 3 cube cities.");
            return false;
        }
    }
    
    public boolean go2CubeCities()
    {        
        City[] cube2Cities = pandemicBoard.get2CubeCities();
        if (cube2Cities.length > 0)
        {
            //System.out.print("Setting 2 cube cities -");
            for (int i = 0 ; i < cube2Cities.length ; i ++)
            {
                //System.out.print(" " + cube2Cities[i].getName());
            }
            getDistances(cube2Cities);
            //System.out.println(" as destinations.");
            City toDriveTo = calculateDestination();
            //System.out.println(this.getPlayerName() + " will go to " + toDriveTo.getName());
            driveCity(playerPiece.getLocation(),toDriveTo);
            return true;
        }
        else
        {
            //System.out.println("No 2 cube cities.");
            return false;
        }
    }       
    
        public boolean go1CubeCities()
    {        
        City[] cube1Cities = pandemicBoard.get1CubeCities();
        if (cube1Cities.length > 0)
        {
            //System.out.print("Setting 1 cube cities -");
            for (int i = 0 ; i < cube1Cities.length ; i ++)
            {
                //System.out.print(" " + cube1Cities[i].getName());
            }
            getDistances(cube1Cities);
            //System.out.println(" as destinations.");
            City toDriveTo = calculateDestination();
            //System.out.println(this.getPlayerName() + " will go to " + toDriveTo.getName());
            driveCity(playerPiece.getLocation(),toDriveTo);
            return true;
        }
        else
        {
            //System.out.println("No 1 cube cities.");
            return false;
        }
    }       
}


