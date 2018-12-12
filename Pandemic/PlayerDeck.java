
/**
 * Write a description of class PlayerDeck here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Collections;

public class PlayerDeck extends Deck
{
    // instance variables - replace the example below with your own
    public PlayerCard[] cards;

    /**
     * Constructor for objects of class PlayerDeck
     */
    public PlayerDeck(String currentPlayerDeckName, int size)
    {
        super(currentPlayerDeckName);
        cards = new PlayerCard[size];
    }
    
    public int findNextNull ()
    {
        for (int i = 0 ; i< cards.length ; i ++)
        {
            if (cards[i]==null)
            {
                return i;
            }
        }
        return 999999999;
    }
    
    public int findNextNonNull ()
    {
                for (int i = 0 ; i< cards.length ; i ++)
        {
            if (cards[i]!=null)
            {
                return i;
            }
        }
        return 999999999;
    }

    public void addCardTop (PlayerCard toAdd)
    {
        addCardPos(toAdd, 0);
    }
    
    public void addCardBottom (PlayerCard toAdd)
    {
        addCardPos(toAdd, this.getSize());
        
    }
    
    public void addCardPos (PlayerCard toAdd, int position)
    {
        PlayerCard[] newCards = new PlayerCard[cards.length+1];
        for (int i = 0 ; i < position ; i ++)
        {
            // System.out.println("adding to " + i );
            newCards[i] = cards[i];
        }
        // System.out.println("ADDING GIVEN CARD to " + position);
        newCards[position] = toAdd;
        for (int i = position + 1 ; i < newCards.length ; i ++)
        {
            // System.out.println("adding further new cards to " + i);
            newCards[i] = cards[i-1];
        }
        cards = newCards;
        removeNulls();
    }
    
    public PlayerCard drawTop (Player drawingPlayer)
    {
        PlayerCard toReturn;
        int cardPosition = findNextNonNull();
        toReturn = cards[cardPosition];
        removeCardInt(cardPosition);
        removeNulls();
        return toReturn;
    }
    
    public void removeNulls()
    {
        PlayerCard[] firstArray = cards;
        List<PlayerCard> list = new ArrayList<PlayerCard>();
        for(PlayerCard k : firstArray)
        {
            if (k != null)
            {
                list.add(k);
            }
            firstArray = list.toArray(new PlayerCard[list.size()]);
            cards = firstArray;
            
        }
        
    }
    
    public PlayerCard drawBottom ()
    {
        PlayerCard toReturn;
        toReturn = cards[cards.length-1];
        return toReturn;
    }
    
    public int getSize()
    {
        return cards.length;
    }
    
    public void shuffle()
    {
        List shuffledDeckList;
        shuffledDeckList = Arrays.asList(cards);
        Collections.shuffle(shuffledDeckList);
    }

    
    public void removeCardInt (int toRemove)
    {
        cards[toRemove] = null;
        removeNulls();
        
    }
    
}
