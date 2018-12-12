
/**
 * Write a description of class ResearchCentre here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class ResearchCentre
{
    // instance variables - replace the example below with your own
    public City location;

    /**
     * Constructor for objects of class ResearchCentre
     */
    public ResearchCentre(City currentLocation)
    {
        // initialise instance variables
        location = currentLocation;
    }

    /**
     * An example of a method - replace this comment with your own
     * 
     * @param  y   a sample parameter for a method
     * @return     the sum of x and y 
     */
    public void setLocation(City newLocation)
    {
        // put your code here
        location = newLocation;
    }
    
        public City getLocation()
    {
        // put your code here
        return location;
    }
}
