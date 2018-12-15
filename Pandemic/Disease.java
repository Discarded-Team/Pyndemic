
/**
 * Write a description of class Disease here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Disease
{
    // instance variables - replace the example below with your own
    public String colour;
    public boolean cured;
    public boolean eliminated;


    /**
     * Constructor for objects of class Disease
     */
    public Disease(String diseaseColour)
    {
        colour = diseaseColour;
        cured = false;
        eliminated = false;
        
    }
    
    public boolean getCured()
    {
        return cured;
    }
    
    public void setCured(boolean toSet)
    {
        cured = toSet;
    }

    public void setColour(String newColour)
    {
        colour = newColour;
    }
    
    public String getColour()
    {
        return colour;
    }
    
    
}
