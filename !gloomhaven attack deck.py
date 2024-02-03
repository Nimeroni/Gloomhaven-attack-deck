# I, the copyright holder of this work, release this work into the public domain. This applies worldwide.
#
# In some countries this may not be legally possible; if so:
# I grant anyone the right to use this work for any purpose, without any conditions, unless such conditions are required by law.
 
# Version 0.0.4
 
import sys
import random
 
misses = 0.0
 
# Return the value of an attack, given a base attack value, the card drawn, the deck of remaining cards and the discard pile.
# Also returns the deck with the card removed and all the discarded cards, including the card being considered.
def cardValue(base, card, deck, discard, truesight = False):
    global misses
    discard.append(card)
 
    if card == '0':
        return base 
    elif card == '+1':
        return base + 1
    elif card == '-1':
        if truesight : #Truesight lense from FH. It set negative modifier to 0.
            return base
        return base - 1
    elif card == '+2':
        return base + 2
    elif card == '-2':
        if truesight : #Truesight lense from FH. It set negative modifier to 0.
            return base
        return base - 2
    elif card == 'MISS':
        deck += discard
        random.shuffle(deck)
        assert len(deck) == len(amd)
        discard[:] = []
        if truesight : #Truesight lense from FH. It set negative modifier to 0.
            return base
        misses += 1
        return 0
    elif card == 'CURSE':
        if truesight : #Truesight lense from FH. It set negative modifier to 0.
            return base
        misses += 1
        return 0        
    elif card == '2x':
        deck += discard
        random.shuffle(deck)
        assert len(deck) == len(amd)
        discard[:] = []
        return 2*base
    elif card == 'BLESS':
        return 2*base
    elif card == 'R+1':
        card2 = deck.pop()
        return cardValue(base+1,card2,deck,discard)
    elif card == 'R+0':
        card2 = deck.pop()
        return cardValue(base,card2,deck,discard)
    else:
        raise ValueError            
 
# Return the value of an attack with advantage, given a base attack value, the cards drawn, the deck of remaining cards and the 
# discard pile.  Also returns the deck with the cards removed and all the discarded cards, including the cards being considered.
def advantageValue(base,card1, card2, deck, discard, truesight = False):
    if card1 == 'R+1':
        discard.append(card1)
        return cardValue(base+1,card2,deck,discard,truesight)
    elif card2 == 'R+1':
        discard.append(card2)
        return cardValue(base+1,card1,deck,discard,truesight)
    if card1 == 'R+0':
        discard.append(card1)
        return cardValue(base,card2,deck,discard,truesight)
    elif card2 == 'R+0':
        discard.append(card2)
        return cardValue(base,card1,deck,discard,truesight)
    elif card1 == 'MISS':
        discard.append(card1)
        cv = cardValue(base,card2,deck,discard,truesight)
        deck += discard
        random.shuffle(deck)
        assert len(deck) == len(amd)
        discard[:] = []
        return cv
    elif card2 == 'MISS':
        discard.append(card2)
        cv = cardValue(base,card1,deck,discard,truesight)
        deck += discard
        random.shuffle(deck)
        assert len(deck) == len(amd)
        discard[:] = []
        return cv
    elif card1  == 'CURSE':
        discard.append(card1)
        cv = cardValue(base,card2,deck,discard,truesight)
        return cv
    elif card2  == 'CURSE':
        discard.append(card2)
        cv = cardValue(base,card1,deck,discard,truesight)
        return cv

 
    discard.append(card1)
    discard.append(card2)
 
    assert len(deck)+len(discard) == len(amd)
 
    if card1 == '2x' or card2 == '2x':
        deck += discard
        random.shuffle(deck)
        assert len(deck) == len(amd)
        discard[:] = []
        return 2*base
    elif card1 == 'BLESS' or card2 == 'BLESS':
        return 2*base
    
    elif card1 == '+2' or card2 == '+2':
        return 2+base
    elif card1 == '+1' or card2 == '+1':
        return 1+base
    elif card1 == '0' or card2 == '0':
        return base
    elif card1 == '-1' or card2 == '-1':
        if truesight : #Truesight lense from FH. It set negative modifier to 0.
            return base
        return base - 1
    
    assert card1 == '-2' or card2 == '-2'
    if truesight:  # Truesight lense from FH. It set negative modifier to 0.
        return base
    return base - 2
    

# Return the value of an attack with disadvantage, given a base attack value, the cards drawn, the deck of remaining cards and the 
# discard pile.  Also returns the deck with the cards removed and all the discarded cards, including the cards being considered.
def disadvantageValue(base,card1, card2, deck, discard, truesight = False):
    global misses
    
    if card1 == 'MISS' or card2 == 'MISS':
        discard.append(card1)
        discard.append(card2)
        deck += discard
        random.shuffle(deck)
        assert len(deck) == len(amd)
        discard[:] = []
        if truesight : #Truesight lense from FH. It set negative modifier to 0.
            return base
        misses += 1
        return 0
    if card1 == 'CURSE' or card2 == 'CURSE':
        discard.append(card1)
        discard.append(card2)
        # We still need to shuffle if the 2nd card is a 2x, even without using it
        if card1 == '2x' or card2 == '2x':
            deck += discard
            random.shuffle(deck)
            assert len(deck) == len(amd)
            discard[:] = []
        if truesight : #Truesight lense from FH. It set negative modifier to 0.
            return base
        misses += 1
        return 0
    elif card1 == 'R+1':
        discard.append(card1)
        return cardValue(base+1,card2,deck,discard,truesight)
    elif card2 == 'R+1':
        discard.append(card2)
        return cardValue(base+1,card1,deck,discard,truesight)
    if card1 == 'R+0':
        discard.append(card1)
        return cardValue(base,card2,deck,discard,truesight)
    elif card2 == 'R+0':
        discard.append(card2)
        return cardValue(base,card1,deck,discard,truesight)

 
    discard.append(card1)
    discard.append(card2)

    # Even if we don't use the 'x2', we still need to reshuffle
    if card1 == '2x' or card2 == '2x': 
        deck += discard
        random.shuffle(deck)
        assert len(deck) == len(amd)
        discard[:] = []
 
    assert len(deck)+len(discard) == len(amd)
 
    if card1 == '-2' or card2 == '-2':
        if truesight : #Truesight lense from FH. It set negative modifier to 0.
            return base
        return base - 2
    elif card1 == '-1' or card2 == '-1':
        if truesight : #Truesight lense from FH. It set negative modifier to 0.
            return base
        return base - 1
    elif card1 == '0' or card2 == '0':
        return base
    elif card1 == '+1' or card2 == '+1':
        return 1+base
    elif card1 == '+2' or card2 == '+2':
        return 2+base

    # You need either one 2x and one bless or 2 bless
    assert (card1 == '2x' or 'BLESS') and (card2 == '2x' or 'BLESS')
    return 2*base
 
# Given an attack modifier deck, amd, determine the average attack value with and without advantage.
# Optionally takes a base attack value, defaulting to 3 if none is provided.
def calculateAverageAttack(amd, base = None, normal = True, advantage = False, disadvantage = False, truesight = False):
    global misses
    if base is None:
        base = 3
    deck = list(amd)
    random.shuffle(deck)
    discard = []
    
    count = 1000000

    # Run without advantage or disadvantage
    if normal == True:
        total = 0.0 # A running total of the all "damage" calculated
        misses = 0.0
        
        for x in range(0,count):
            card = deck.pop()
            total = total + cardValue(base, card, deck, discard, truesight)
 
        print ("Average attack:  ", (total / count))    # the average attack value
        print ("Miss frequency:  ", (misses/count)) # percent of attacks that pull a null or curse


    # Run with advantage
    if advantage == True:
        # reset
        total = 0.0
        misses = 0.0  
        deck += discard 
        random.shuffle(deck)
        discard[:] = []
 
        for x in range(0,count):
            card1 = deck.pop()
            card2 = deck.pop()
            total = total + advantageValue(base, card1,card2, deck,discard, truesight);
 
        print ("Average attack with advantage:  ",total / count)  # the average attack value
        print ("Miss frequency:  ", misses/count) # percent of attacks that pull a null or curse

    # Run with disadvantage
    if disadvantage == True:
        # reset
        total = 0.0
        misses = 0.0  
        deck += discard 
        random.shuffle(deck)
        discard[:] = []
 
        for x in range(0,count):
            card1 = deck.pop()
            card2 = deck.pop()
            total = total + disadvantageValue(base, card1, card2, deck, discard, truesight);
 
        print ("Average attack with disadvantage:  ",total / count)  # the average attack value
        print ("Miss frequency:  ", misses/count) # percent of attacks that pull a null or curse
    
'''
# Basic attack deck
amd = ['0','0','0','0','0','0','+1','+1','+1','+1','+1','-1','-1','-1','-1','-1','-2','+2','MISS','2x']
print ("   Base attack deck")
print (amd)
calculateAverageAttack(amd, advantage = True, disadvantage = True)

# Fully cursed deck
amd = ['0','0','0','0','0','0','+1','+1','+1','+1','+1','-1','-1','-1','-1','-1','-2','+2','MISS','2x','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE']
print ("   Ten curses")
print (amd)
calculateAverageAttack(amd, disadvantage = True)

# Basic attack deck  with truesight
amd = ['0','0','0','0','0','0','+1','+1','+1','+1','+1','-1','-1','-1','-1','-1','-2','+2','MISS','2x']
print ("   Base attack deck with truesight lense")
print (amd)
calculateAverageAttack(amd, advantage = True, disadvantage = True, truesight = True)

# Fully cursed deck
amd = ['0','0','0','0','0','0','+1','+1','+1','+1','+1','-1','-1','-1','-1','-1','-2','+2','MISS','2x','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE']
print ("   Ten curses with truesight lense")
print (amd)
calculateAverageAttack(amd, advantage = True, disadvantage = True, truesight = True)
'''

# Blinkblade attack deck
amd = ['0','0','0','0','+2','+2','+1','+1','+1','+1','+1','-1','0','0','+1','+1','+2','MISS','2x']
print ("   BB attack deck")
print (amd)
calculateAverageAttack(amd, base = 7, advantage = True, disadvantage = True)

# Blinkblade attack deck with truesight
amd = ['0','0','0','0','+2','+2','+1','+1','+1','+1','+1','-1','0','0','+1','+1','+2','MISS','2x']
print ("   BB attack deck with truesight")
print (amd)
calculateAverageAttack(amd, base = 7, advantage = True, disadvantage = True, truesight = True)

# Blinkblade attack deck on a fully cursed deck
amd = ['0','0','0','0','+2','+2','+1','+1','+1','+1','+1','-1','0','0','+1','+1','+2','MISS','2x','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE']
print ("   BB attack deck with 10 curses")
print (amd)
calculateAverageAttack(amd, base = 7, advantage = True, disadvantage = True)

# Blinkblade attack deck on a fully cursed deck with truesight
amd = ['0','0','0','0','+2','+2','+1','+1','+1','+1','+1','-1','0','0','+1','+1','+2','MISS','2x','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE','CURSE']
print ("   BB attack deck with 10 curses with truesight lense")
print (amd)
calculateAverageAttack(amd, base = 7, advantage = True, disadvantage = True, truesight = True)
