import collections
import random

Card = collections.namedtuple('Card', ['rank', 'suit'])
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
class FrenchDeck(object):
    """docstring for FrenchDeck"""
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def spades_high(self, card):
        rank_value = self.ranks.index(card.rank)
        print 'rank_value = %s, card.rank = %s' % (rank_value, card.rank)
        print 'ret = %d, card.suit = %s' % (rank_value * len(suit_values) + suit_values[card.suit], card.suit)
        return rank_value * len(suit_values) + suit_values[card.suit]
if __name__ == '__main__':
    deck = FrenchDeck()
    # print random.choice(deck)
    for card in sorted(deck, key=deck.spades_high):
        print card



    
