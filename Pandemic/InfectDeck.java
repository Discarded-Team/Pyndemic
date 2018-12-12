
/**
 * Write a description of class InfectDeck here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Collections;

public class InfectDeck extends Deck
{
    // instance variables - replace the example below with your own
    public InfectCard[] cards;

    /**
     * Constructor for objects of class InfectDeck
     */
    public InfectDeck(String currentInfectDeckName, int size)
    {
        super(currentInfectDeckName);
        cards = new InfectCard[size];
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

    public void addCardTop (InfectCard toAdd)
    {
        addCardPos(toAdd, 0);
    }
    
    public void addCardBottom (InfectCard toAdd)
    {
        addCardPos(toAdd, this.getSize());
        
    }
    
    public void addCardPos (InfectCard toAdd, int position)
    {
        InfectCard[] newCards = new InfectCard[cards.length+1];
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
    
    public InfectCard drawTop (InfectDeck discardPile)
    {
        InfectCard toReturn;
        int cardPosition = findNextNonNull();
        toReturn = cards[cardPosition];
        discardPile.addCardTop(toReturn);
        removeCardInt(cardPosition);
        removeNulls();
        return toReturn;
    }
    
        public InfectCard drawBottom (InfectDeck discardPile)
    {
        InfectCard toReturn;
        int cardPosition = cards.length-1;
        toReturn = cards[cardPosition];
        discardPile.addCardTop(toReturn);
        removeCardInt(cardPosition);
        removeNulls();
        return toReturn;
    }

    
    public void removeNulls()
    {
        InfectCard[] firstArray = cards;
        List<InfectCard> list = new ArrayList<InfectCard>();
        for(InfectCard k : firstArray)
        {
            if (k != null)
            {
                list.add(k);
            }
            firstArray = list.toArray(new InfectCard[list.size()]);
            cards = firstArray;
            
        }
        
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
