import sys
print(sys.path)
from src.classes import AutoDeck

deck = AutoDeck()
#print(deck.get_cards())
for card in deck.get_cards():
    print(card.front)
    print(card.back)
    print()

print([cards.front for cards in deck.get_cards('frasesTeste.txt')])