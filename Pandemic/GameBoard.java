import java.util.Random;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Collections;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

/**
 * This is my attempt at the Pandemic Board game.
   */
public class GameBoard
{
    // An array containing all the city objects used in the game.
    public City[] cities;
    
    // A city used for unused research centres
    public City unplaced = new City(" ", " ");

     // the number of cards needed to discover a cure
    public int neededForCure;
    
    // the array of the infection rate indicator.
    public int[] infectionRate;
    
    // the position on the array of the marker.
    public int currentRate;
    
    // The number of outbreaks.
    public int outbreakCount;
    
    // An array containing all the players pieces.
    public Piece[] playerPieces;    
    
    // A deck made up of player cards.
    public PlayerDeck playerDeck;    
    
    // A deck made up of discarded player cards.
    public PlayerDeck playerDiscard;
    
    
    // The same for the infect cards
    
    public InfectDeck infectDeck;
    public InfectDeck infectDiscard;
    
    // counters for each of the pools of cubes.
    public int redCubes = 40;
    public int blueCubes = 40;
    public int yellowCubes = 40;
    public int blackCubes = 40;
    public int purpleCubes = 40;
    
    // An array containing all the research centres
    public ResearchCentre[] researchCentres;
    
    // An array containing all the diseases used in the game.
    public Disease[] diseases;
    
    public int numberColours;
        
    // This gives a list of all the colours which could be used.
    String[] possibleColour = {"red","blue","yellow","black","purple"};
    
    public GameBoard(int currentNumberColours, int[] gameInfectionRate, 
    int cureRequirement, int epidemics, int currentResearch, int initalResearch, String currentMapLocation)
    {
        infectionRate = gameInfectionRate;
        currentRate = 0;
        setDiseases(currentNumberColours);
        System.out.println("Setting up the map");
        setGivenCSV(currentMapLocation);
        setResearchCentres(currentResearch, initalResearch);
        setPlayerCardDeck(epidemics);
        playerPieces = new Piece[6];
        outbreakCount = 0;
        neededForCure = cureRequirement; 
        numberColours = currentNumberColours;
    }
    
    public ResearchCentre[] getResearchCentre()
    {
        return researchCentres;
    }
    
    public int getNumberColours()
    {
        return numberColours;
    }
    
    public int getNeededForCure()
    {
        return neededForCure;
    }
    
    public String getGameState()
    {
        return current3CubeCities();

    }
    
    
    // returns all the cities with 3 cubes
    public City[] get3CubeCities()
    {
        City[] toReturn = new City[countXCubeCities(cities, 3)];
        int addPos = 0;
        for (int i = 0 ; i < cities.length ; i ++)
        {
            if (cities[i].getMaxCube() == 3)
            {
                toReturn[addPos] = cities[i];
                addPos++;
            }
        }       
        return toReturn;
    }

    // returns all the cities with 2 cubes
    public City[] get2CubeCities()
    {
        City[] toReturn = new City[countXCubeCities(cities, 2)];
        int addPos = 0;
        for (int i = 0 ; i < cities.length ; i ++)
        {
            if (cities[i].getMaxCube() == 2)
            {
                toReturn[addPos] = cities[i];
                addPos++;
            }
        }       
        return toReturn;
    }
    
        // returns all the cities with 2 cubes
    public City[] get1CubeCities()
    {
        City[] toReturn = new City[countXCubeCities(cities, 1)];
        int addPos = 0;
        for (int i = 0 ; i < cities.length ; i ++)
        {
            if (cities[i].getMaxCube() == 1)
            {
                toReturn[addPos] = cities[i];
                addPos++;
            }
        }       
        return toReturn;
    }
    
    
    public City[] getResearchLocations()
    {
        City[] toReturn = new City[researchCentres.length];
        for (int i = 0 ; i < researchCentres.length ; i ++)
        {
            toReturn[i] = researchCentres[i].getLocation();
        } 
        return toReturn;
    }
    
    public String current3CubeCities()
    {

        String toReturn = "";
        City[] toUse = get3CubeCities();
        for (int i = 0; i < toUse.length; i ++)
        {
            toReturn = toReturn + toUse[i].getName() + " ";
        }
        return toReturn + " these cities have 3 cubes";
    }
    
    // returns an int equal to the number of cities with X cubes in
    public int countXCubeCities(City[] cityArray, int numberCubes)
    {
        int toReturn = 0;
        for (int i = 0; i < cities.length; i++)
        {
            // System.out.println("looking for cities with X cubes");
            if (cities[i].getMaxCube() == numberCubes)
            {
                // System.out.println("found a city with X cubes!");
                toReturn++;
            }            
        }
        return toReturn;
    }
            
    public int getInfectionRate()
    {
        return infectionRate[currentRate];
    }
    
    public int getOutbreakCount()
    {
        return outbreakCount;
    }
    
    // Increments the outbreak counter
    public void incrementOutbreak()
    {
        outbreakCount++;
    }
    
    public void shuffleInEpidemics(int epidemicsCount)
    {
        int decksize = playerDeck.getSize();
        int cardsInPile;
        int putEpidemic;
        int decidedEpidemics = 0;
        int[] epidemicPlaces = new int[epidemicsCount];
        System.out.println("There are " + decksize + " cards in the player deck");
        cardsInPile = decksize / epidemicsCount;
        System.out.println("Putting " + cardsInPile + " in a pile");
        for (int i = 0 ; i < epidemicsCount ; i ++ )
        {
            putEpidemic = shuffleToPos(cardsInPile)+(i*cardsInPile);
            System.out.println("Epidemic : "+ i +" at " +  putEpidemic);
            epidemicPlaces[decidedEpidemics] = putEpidemic;
            decidedEpidemics++;
            
        }
        addEpidemicToPlayerDeck(epidemicPlaces, epidemicsCount);
    }
    
    
    /**
     * This bit of code works, but is horrific. It's a 
     * bunch of loops to place the epidemics into the 
     * player deck at game start.
     */ 
    public void addEpidemicToPlayerDeck(int[] epidemicPlaces, int epidemicsCount)
    {
        for (int i = 0 ; i < epidemicsCount ; i++)
        {
            PlayerCard epidemicCard = new PlayerCard(true);
            playerDeck.addCardPos(epidemicCard, epidemicPlaces[i]+i);
        }
    }
    
    // A tiny bit of sensible code breaking down the above method.
    public int shuffleToPos(int shuffleToPos)
    {
        Random rand = new Random();        
        int n = rand.nextInt(shuffleToPos);
//        System.out.println("I've decided to put the epidemic " + n + " from the top");
        return n;
        
        
    }
    
    public void addPlayerCardDiscard(PlayerCard toAdd)
    {
        playerDiscard.addCardTop(toAdd);
    }
    
    public void startGame(int[] initalInfectStep)
    {
        setInfectCardDeck();
        initalInfect(initalInfectStep[0],initalInfectStep[1],initalInfectStep[2]);        
    }
    
    // This method will infect a given number of cities based on the given infection rate.
    public void infectCityPhase(int infectionRate)
    {
        int i;
        i = 0;
        while (i< infectionRate)
        {
            i = i + 1;
            String[] cityToInfect = infectDeck.drawTop(infectDiscard).getCard();
            System.out.println("INFECTING " + cityToInfect[0] + " with " + cityToInfect[1] + " cubes.");
            infectCity(cityToInfect[0],cityToInfect[1]);
        }
    }
    
    // Sets up the inital outbreaks of disease for a given number of each city.
    public void initalInfect(int threecities, int twocities, int onecities )
    {
        // loop for the 3 cards to be drawn for 3 counters
        for (int i = threecities; i> 0; i--)
        {
            // Draws a card to have 3 cubes placed on it
            String[] toInfect=infectDeck.drawTop(infectDiscard).getCard();

            for (int x = 3; x > 0; x --)
            {
                // System.out.println("Placing " + x + " cube on " + toInfect[0]);
                infectCity(toInfect[0],toInfect[1]);
            }
        }

        // loop for the given cards to be drawn for 2 counters
                for (int i = twocities; i> 0; i--)
        {
            // Draws a card to have 3 cubes placed on it
            String[] toInfect=infectDeck.drawTop(infectDiscard).getCard();

            for (int x = 2; x > 0; x --)
            {
                // System.out.println("Placing " + x + " cube on " + toInfect[0]);
                infectCity(toInfect[0],toInfect[1]);
            }
        }
        
        // loop for the given cards to be drawn for 1 counter
                for (int i = onecities; i> 0; i--)
        {
            // Draws a card to have 3 cubes placed on it
            String[] toInfect=infectDeck.drawTop(infectDiscard).getCard();

            for (int x = 1; x > 0; x --)
            {
                // System.out.println("Placing " + x + " cube on " + toInfect[0]);
                infectCity(toInfect[0],toInfect[1]);
            }
        }
        
    }
    
    // Infects a given city with a cube of the given colour
    public void infectCity(String infectCity, String cubeColour)
    {
        int cityPosition;
        List cityList;
        cityList = Arrays.asList(cities);
        // Finds the position of the city to be infected in the cities array.
        cityPosition = findCityPosition(infectCity);
        // System.out.println("I have found " + infectCity + "and think it is at position " + cityPosition + " within the cities arrary");
        if (cities[cityPosition].addCube(cubeColour))
        {
            System.out.println("OUTBREAK");
            incrementOutbreak();
        }        
        // removes a cube of the appropriate colour from the game boards pool.
        removeCube(cubeColour);
        // System.out.println("Just removed a " + cubeColour + " from the pool");
    }
    
    public void resetDistances()
    {
        for (int i = 0 ; i < cities.length ; i ++)
        {
            cities[i].setDistance(9999999);
        }
    }
    
    
    // returns an int representing the place in the cities array of a given City
    public int findCityPosition(String cityName)
    {
        int i = 0;
        while (i < 100)
        {
            if (cities[i].getName().equals(cityName))
            {
                return i;
            }
            i = i+1;
        }
        return 0;
    }

    // takes a cube away from the pool of cubes.
    public void removeCube(String Cubecolour)
    {
        if (Cubecolour.equals("red"))
        {
            redCubes = redCubes - 1;
        }
        else if (Cubecolour.equals("blue"))
        {
            blueCubes = blueCubes - 1;
        }        
        else if (Cubecolour.equals("yellow"))
        {
            yellowCubes = yellowCubes - 1;
        }   
        else if (Cubecolour.equals("black"))
        {
            blackCubes = blackCubes - 1;
        }   
        else if (Cubecolour.equals("purple"))
        {
            purpleCubes = purpleCubes - 1;
        }   
        checkCubesRemain();
    }
    
    // checks the game isn't lost because disease cubes have run out (unfinished)
    public void checkCubesRemain()
    {
        // NEEDS TO BE WRITTEN
    }
    
    
        // This returns the number of non Null entries as an int for Infection Cards.
    public int nonNullCountPlayer (PlayerCard[] arrayToCount)
    {
        int toReturn = 0;
        for (int i = 0; i < arrayToCount.length; i++)
        {
            if (arrayToCount[i] != null)
            {
                toReturn++;
            }
        }
        return toReturn;
    }
    
    // This returns the number of non Null entries as an int for Infection Cards.
    public int nonNullCount (InfectCard[] arrayToCount)
    {
        int toReturn = 0;
        for (int i = 0; i < arrayToCount.length; i++)
        {
            if (arrayToCount[i] != null)
            {
                toReturn++;
            }
        }
        return toReturn;
    }
    
    public boolean emptyDeck ()
    {
        int cardsLeft;
        cardsLeft = playerDeck.getSize();
        if (cardsLeft == 0)
        {
            return true;
        }
        else
        {
            return false;
        }
    }


    
    // moves the infection rate marker by 1.
    public void increaseEpidemic()
    {
        currentRate++;
        System.out.println("Increasing the rate of infection");
    }
    
    //draws the bottom card of the infection deck, and places 3 cubes on it.
    public void infectEpidemic()
    {
        String[] toInfect;
        toInfect = infectDeck.drawBottom(infectDiscard).getCard();
        System.out.println(toInfect[0] + " has now been infected with 3 cubes.");
        for (int i=3;i>0;i--)
        {
            // System.out.println("infecting " + toInfect[0] + " as the bottom card for " + (4-i)  + " time");
            infectCity(toInfect[0],toInfect[1]);
        }
    }
        
    // removes nulls from infect card arrays
    public InfectCard[] removeNulls(InfectCard[] infectCardArray)
    {
        InfectCard[] firstArray = infectCardArray;
        List<InfectCard> list = new ArrayList<InfectCard>();
        for(InfectCard k : firstArray )
        {
            if(k != null)
            {
                list.add(k);
            }
        }
        firstArray = list.toArray(new InfectCard[list.size()]);
        return firstArray;
    }
    
    // shuffles the infection discard pile onto the top of the infection deck
    public void intensifyEpidemic()
    {
        infectDiscard.shuffle();
        for (int i = 0 ; i < infectDiscard.getSize() ; i ++)
        {
            infectDeck.addCardTop(infectDiscard.cards[i]);
        }
        infectDiscard = new InfectDeck("infectDiscard",0);
    }
    
    public void resolveEpidemic()
    {
        // moves the infection rate marker by 1, and updates the rate.
        increaseEpidemic();
        // draws the bottom card of the infection deck, and places 3 cubes on it
        infectEpidemic();
        // shuffles the infection discard pile onto the top of the infection deck
        intensifyEpidemic();
    }
        
    
        public void setPlayerCardDeck(int epidemics)
    {
        int i;
        playerDeck = new PlayerDeck("playerDeck",1);
        i = cities.length;
        while (i > 0)
        {
            // System.out.println("Adding " + cities[i-1].getName());
            playerDeck.addCardTop(new PlayerCard(cities[i-1].getName(), cities[i-1].getColour()));
            i = i-1;
        }
        playerDeck.shuffle();
        playerDiscard = new PlayerDeck("playerDiscard",1);
    }
    
    // sets up the infection card deck based on the cities array
        public void setInfectCardDeck()
    {
        int i;
        infectDeck = new InfectDeck("infectDeck",1);
        i = cities.length;
        while (i > 0)
        {
            // System.out.println("Adding " + cities[i-1].getName());
            infectDeck.addCardTop(new InfectCard(cities[i-1].getName(), cities[i-1].getColour()));
            i = i-1;
        }
        infectDeck.shuffle();
        infectDiscard = new InfectDeck("infectDiscard",1);
    }
    
    

    /**
     * Constructor for objects of class GameBoard
     */
    public void setDiseases(int currentNumberColours)
    {
        int i;
        i = currentNumberColours;
        Disease[] disToUse = new Disease[currentNumberColours];
        while (i > 0)
        {
            disToUse[i-1] = new Disease(possibleColour[i-1]);
            i = i-1;
        }
        
        // This sets the array of diseases used to the values generated above.
        diseases = disToUse;
        
    }
    
    public boolean cureDisease(String colour)
    {
        Disease toCure = getDisease(colour);
        if (!toCure.getCured())
        {
            toCure.setCured(true);
            System.out.println("Cured " + toCure.getColour());
            return true;
        }
        System.out.println("already cured!");
        return false;
        
        
    }
    
    public Disease getDisease(String colour)
    {
        for (int i = 0; i < diseases.length ; i ++)
        {
            if (diseases[i].getColour().equals(colour))
            {
                return diseases[i];
            }
        }
        return null;
    }
        
    public ArrayList getCSVCol(int col, String fileLoc)
    {
        ArrayList<String> ar = new ArrayList<String>();

        File file = new  File("/home/joe/Documents/OU/Year2.0/M250/Pandemic8/" + fileLoc);
        try
        {
            Scanner inputStream = new Scanner(file);
            inputStream.next(); // ignore first line
            while (inputStream.hasNext())
            {
                String data = inputStream.next();
                // System.out.println("Here is the raw data " + data);
                String[] values = data.split(",");
                // System.out.println("Here is the value "+ values); 
                ar.add(values[col]);
            }
            inputStream.close();
        }
        catch (FileNotFoundException e)
        {
            System.out.println("ERM!");
        }
        return ar;
        
    }

    
        public ArrayList getCSVCols(String fileLoc)
    {
        ArrayList<String> ar = new ArrayList<String>();

        File file = new  File("/home/joe/Documents/OU/Year2.0/M250/Pandemic8/" + fileLoc);
        try
        {
            Scanner inputStream = new Scanner(file);
            inputStream.next(); // ignore first line
            while (inputStream.hasNext())
            {
                String data = inputStream.next();
                // System.out.println("Here is the raw data " + data);
                String[] values = data.split(",");
                // System.out.println("Here is the value "+ values); 
                ar.add(values[2]+","+values[3]+","+values[4]+","+values[5]+","+values[6]+","+values[7]);
            }
            inputStream.close();
        }
        catch (FileNotFoundException e)
        {
            System.out.println("ERM!");
        }
        return ar;
        
    }
    
    public void setGivenCSV (String fileLoc)
    {
        String[] deleteMe = new String[0];
        
        // creates an array of names
        ArrayList<String> namesAL = new ArrayList<String>();
        namesAL = getCSVCol(0,"cities.csv");
        String[] namesArray = namesAL.toArray(new String[namesAL.size()]);
        
        // System.out.println("here is okay");
        // creates an array of colours
        ArrayList<String> colourAL = new ArrayList<String>();
        colourAL = getCSVCol(1,"cities.csv");
        String[] colourArray = colourAL.toArray(new String[colourAL.size()]);

        
        
        City[] draftCities = new City[namesAL.size()];
        for (int i = 0 ; i < namesAL.size() ; i ++)
        {
            draftCities[i] = new City(namesArray[i],colourArray[i]);
        }
        cities = draftCities;
        
        // creates an array of connections
        ArrayList<String[]> connectionAL = new ArrayList<String[]>();
        connectionAL = getCSVCols("cities.csv");
        String[] connectionArray = connectionAL.toArray(new String[connectionAL.size()]);

        
        for (int i = 0 ; i < connectionAL.size() ; i ++)
        {
            City[] toConnect = new City[6];
            for (int x = 0 ; x<6 ; x ++)
            {
                // System.out.println("connection name " + connectionArray[i].split(",")[x]);
                if (connectionArray[i].split(",")[x].equals("x"))
                {
                    // System.out.println("no connection");
                    toConnect[x] = unplaced;

                }
                else
                {
                    // System.out.println("setting connection to " + findCityPosition(connectionArray[i].split(",")[x]));
                    toConnect[x] = cities[findCityPosition(connectionArray[i].split(",")[x])];
                    
                }
            }
            cities[i].setConnections(toConnect);
        }

    }
    
    public void setSouthEngland()
    {
                /**
            * This long list of cities seems really ineficient, there must be
            * an easier way to load these details from a .CSV file.
            */
        City weymouth = new City("Weymouth", "red");
        City poole = new City ("Poole","yellow");
        City worthing = new City ("Worthing","yellow");
        City[] citiestouse = {weymouth, poole, worthing};
        cities = citiestouse;
    }
    
    public void setPlayerStart()
    {
        int i;
    }
    
    public void setResearchCentres( int initalResearch, int numberResearch)
    {
        System.out.println("I have initalResearch " + initalResearch);
        int i;
        i = numberResearch;
        ResearchCentre[] researchCentreToUse = new ResearchCentre[i];
        while (i > 0)
        {
            researchCentreToUse[i-1] = new ResearchCentre(unplaced);
            i = i-1;
        }
        researchCentres = researchCentreToUse;
        placeInital(initalResearch);
    }
    
    public void placeInital(int initalResearch)
    {
        System.out.println("Setting inital station");
        for (int i = 0 ; i < initalResearch ; i ++)
        {
            System.out.println("setting a new station in " + cities[i].getName());
            researchCentres[i].setLocation(cities[i]);
        }
    }
    
    public boolean checkResearchStation(City toCheck)
    {
        for (int i = 0 ; i < researchCentres.length ; i ++)
        {
            if (researchCentres[i].getLocation().equals(toCheck))
            {
                return true;
            }
        }
        return false;        
    }
    
    public void setUnplacedResearch(City location)
    {
        for (int i = 0 ; i < researchCentres.length ; i ++)
        {
            if (researchCentres[i].getLocation().getName().equals(" "))
            {
                System.out.println("Placing a new station in " + location.getName() + ".");
                researchCentres[i].setLocation(location);
                break;
            }
            
        }
    }
    

}
