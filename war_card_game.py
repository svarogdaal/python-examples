# Author: Silviu Velica
# Date: August 2016
# Description:
#    This is a simple card game (War) implemented in python using classes.
#    The opponent is the computer (P2). The user simply needs to press Return (or Enter).
#    When one player has 0 cards left, he loses.


from random import shuffle
from sys import exit

print "\tAre you ready for war?"
raw_input()

# I added 0, 1, and 11 to have a continuous indexing of the cards and their values
card_order = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "J", "Q", "K", "A"]

# generating a pack of cards with a shuffle function
class Pack(object):
    
    cards = []
    
    def __init__(self):
        for num in ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]:
            for card_type in [" of clubs", " of hearts", " of diamonds", " of spades"]:
                num = str(num)
                self.cards.append(num + card_type)
    
    def shuffle_cards(self):
        shuffle(self.cards)
        

class Player(object):
    
    def __init__(self, hand):
        self.hand = hand


class Distributor(object):
    
    hand1 = []
    hand2 = []
    
    def distribute(self, cards):
        while len(cards) != 0:
            Distributor.hand1.append(cards.pop())
            Distributor.hand2.append(cards.pop())
        return Distributor.hand1, Distributor.hand2


class Play(object):
    
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
    def play_war(self):
        # the algorithm stops when one player is left with 0 cards
        while len(self.p1.hand) != 0 and len(self.p2.hand) != 0:
            c1 = self.p1.hand.pop()
            c2 = self.p2.hand.pop()
            print "P1:", c1
            print "P2:", c2
            v1 = c1.split(' ')
            v2 = c2.split(' ')
            
            # the simple cases first...
            if card_order.index(v1[0]) < card_order.index(v2[0]):
                self.p2.hand.insert(0, c1)
                self.p2.hand.insert(0, c2)
                print "You lose!", "P1:", len(self.p1.hand), "P2:", len(self.p2.hand)
            elif card_order.index(v1[0]) > card_order.index(v2[0]):
                self.p1.hand.insert(0, c2)
                self.p1.hand.insert(0, c1)
                print "You win!", "P1:", len(self.p1.hand), "P2:", len(self.p2.hand)
            else:
                c_down1 = [c1]
                c_down2 =[c2]
                
                # repeating the 'battle' algorithm until the tie is broken or one player loses
                while card_order.index(v1[0]) == card_order.index(v2[0]):
                    
                    if len(self.p1.hand) == 0:
                        print "YOU LOSE WEIRDLY!!!!", len(self.p1.hand), len(self.p2.hand)
                        exit(0)
                    elif len(self.p2.hand) == 0:
                        print "YOU WIN WEIRDLY!!!!", len(self.p1.hand), len(self.p2.hand)
                        exit(0)
                        
                    if len(self.p1.hand) > card_order.index(v1[0]) and len(self.p2.hand) >card_order.index(v1[0]):
                        for i in range(0, card_order.index(v1[0])):
                            d1 = self.p1.hand.pop()
                            d2 = self.p2.hand.pop()
                            c_down1.append(d1)
                            c_down2.append(d2)
                  
                        
                    elif len(self.p1.hand) > len(self.p2.hand):
                        for i in range(0, len(self.p2.hand)):
                            d1 = self.p1.hand.pop()
                            d2 = self.p2.hand.pop()
                            c_down1.append(d1)
                            c_down2.append(d2)
                            
                            
                    else:
                        for i in range(0, len(self.p1.hand)):
                            d1 = self.p1.hand.pop()
                            d2 = self.p2.hand.pop()
                            c_down1.append(d1)
                            c_down2.append(d2)
                    
                    v1 = c_down1[-1].split(' ')
                    v2 = c_down2[-1].split(' ')
                    print "P1 last:", c_down1[-1]
                    print "P2 last:", c_down2[-1]
                    
                if card_order.index(v1[0]) > card_order.index(v2[0]):
                    for c in c_down2:
                        self.p1.hand.insert(0, c)
                    for c in c_down1:
                        self.p1.hand.insert(0, c)
                    print "You win battle!", "P1:", len(self.p1.hand), "P2:", len(self.p2.hand)

                else:
                    for c in c_down1:
                        self.p2.hand.insert(0, c)
                    for c in c_down2:
                        self.p2.hand.insert(0, c)
                    print "You lose battle!", "P1:", len(self.p1.hand), "P2:", len(self.p2.hand)
            raw_input()
            
        if len(self.p1.hand) == 0:
            print "YOU LOSE THE GAME!!!"
        else:
            print "YOU WIN THE GAME!!!"


A = Pack()
A.shuffle_cards()
Distributions = Distributor().distribute(A.cards)
P1 = Player(Distributions[0])
P2 = Player(Distributions[1])
X = Play(P1, P2)
X.play_war()