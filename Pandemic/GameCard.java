
/**
 * Write a description of class InfectCard here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class GameCard
{
    String name;
    String colour;
    /**
     * Constructor for objects of class InfectCard
     */
        public GameCard(String currentName, String currentColour)
    {
        name = currentName;
        colour = currentColour; 
    }
    
            public String getCardName()
    {
        return name;
    }
    
    public String[] getCard()
    {
        String[] toReturn = {name,colour};
        return toReturn;
    }
    
    public String getCardColour()
    {
        return colour;
    }
    
    public boolean thing()
    {
        return true;
    }
    
    public void shuffle()
    {
        System.out.println("done");
    }
}
