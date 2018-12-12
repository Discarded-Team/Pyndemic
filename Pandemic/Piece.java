
/**
 * Write a description of class piece here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Piece
{
    public Player owner;
    public GameBoard gameBoard;
    public City location;


    /**
     * Constructor for objects of class piece
     */
    public Piece(Player newOwner, GameBoard pieceBoard, City currentLocation)
    {
        owner = newOwner;
        gameBoard = pieceBoard;
        location = currentLocation;
        // initialise instance variables
    }
    
    public City getLocationCityFromString(String pieceLocation)
    {
        System.out.println("Getting location from String " + pieceLocation);
        int cityPosition = gameBoard.findCityPosition(pieceLocation);
        System.out.println(cityPosition);
        return gameBoard.cities[cityPosition];
    }
    
    public void setLocation(City newLocation)
    {
        location = newLocation;
    }
    
    public City[] getLocationConnections()
    {
        return location.getConnectedCities();
    }
    
    
        
    public City getLocation()
    {
        return location;
    }
       
}
