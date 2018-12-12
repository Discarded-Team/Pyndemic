
/**
 * Write a description of class PlayerCard here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class PlayerCard extends GameCard
{
    boolean isEpidemic;

    // instance variables - replace the example below with your own


    /**
     * Constructor for objects of class PlayerCard
     */
    public PlayerCard(String currentName, String currentColour)
    {
        super(currentName, currentColour);
    }
    
    public String getName()
    {
        return name;
    }
    
    public PlayerCard(boolean epidemic)
    {
        super("epidemic","epidemic");
        isEpidemic = epidemic;
    }
    
    public boolean isEpidemic()
    {
        return isEpidemic;
    }

}
