
/**
 * Write a description of class City here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class City
{
    // instance variables - replace the example below with your own

    public String name;
    public String colour;
    public int redCubes;
    public int blueCubes;
    public int blackCubes;
    public int yellowCubes;
    public int purpleCubes;
    public int distance;
    public City[] connectedCities;
    public boolean hasOutbreak;
    
    /**
     * Constructor for objects of class City
     */
    public City(String cityName, String cityColour)
    {
        // initialise instance variables
        name = cityName;
        colour = cityColour;
    }
    
    public void setConnections(City[] connections)
    {
        connectedCities = connections;
    }
    
    public void setDistance(int newDistance)
    {
        distance = newDistance;
    }
    
    // returns the highest count of a cube of any colour
    public int getMaxCube()
    {
        return Math.max(Math.max(redCubes,blueCubes),Math.max(Math.max(blackCubes,yellowCubes),purpleCubes));
    }
    
    public String getName()
    {
        return name;
    }
    
    public String getColour()
    {
        return colour;
    }
    
    public int getDistance()
    {
        return distance;
    }
    
    // getter method for connected cities
    public City[] getConnectedCities()
    {
        return connectedCities;
    }
    
    public void removeCube(String cubeColour)
    {
        if (cubeColour.equals("red") && redCubes > 0)
        {
            redCubes = redCubes - 1;
        }
        else if (cubeColour.equals("blue") && blueCubes > 0)
        {
            blueCubes = blueCubes - 1;
        }        
        else if (cubeColour.equals("yellow") && yellowCubes > 0)
        {
            yellowCubes = yellowCubes - 1;
        }   
        else if (cubeColour.equals("black") && blackCubes > 0)
        {
            blackCubes = blackCubes - 1;
        }   
        else if (cubeColour.equals("purple") && purpleCubes > 0)
        {
            purpleCubes = purpleCubes - 1;
        }   
    }
    
        public boolean addCube(String cubeColour)
    {
        if (cubeColour.equals("red"))
        {
            redCubes = redCubes + 1;
        }
        else if (cubeColour.equals("blue"))
        {
            blueCubes = blueCubes + 1;
        }        
        else if (cubeColour.equals("yellow"))
        {
            yellowCubes = yellowCubes + 1;
        }   
        else if (cubeColour.equals("black"))
        {
            blackCubes = blackCubes + 1;
        }   
        else if (cubeColour.equals("purple"))
        {
            purpleCubes = purpleCubes + 1;
        }   
        return checkOutBreaks();
    }
    
    public boolean checkOutBreaks()
    {
        boolean toReturn = false;
        if (redCubes == 4)
        {
            toReturn = true;
            redCubes = 3;
        }
        else if (blueCubes == 4)
        {
            toReturn = true;
            blueCubes = 3;
        }
        else if (yellowCubes == 4)
        {
            toReturn = true;
            yellowCubes = 3;
        }
        else if (blackCubes == 4)
        {
            toReturn = true;
            blackCubes = 3;
        }
        else if (purpleCubes == 4)
        {
            toReturn = true;
            purpleCubes = 3;
        }
        
        return toReturn;
        
    }
    
    public int getCubeColour (String cubeColour)
    {
        if (cubeColour.equals("red"))
        {
            return redCubes;
        }
        else if (cubeColour.equals("blue"))
        {
            return blueCubes;
        }        
        else if (cubeColour.equals("yellow"))
        {
            return yellowCubes;
        }   
        else if (cubeColour.equals("black"))
        {
            return blackCubes;
        }   
        else if (cubeColour.equals("purple"))
        {
            return purpleCubes;
        }   
        return 0;
    }
    
}
