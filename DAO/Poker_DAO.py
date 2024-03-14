import requests


class Poker_DAO():
    """
    """
    def __init__(self):
        self.deck_id = None

    def creation_deck(self):
        """
        """
        response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/")
        deck = response.json()
        self.deck_id = deck["deck_id"]

    def draw(self, deck_id, nbr_carte):
        """
        Tirer 1-2-3 carte(s)
        """
        response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={nbr_carte}")
        tirage = response.json()
        return tirage["cards"]



#P = Poker_DAO()
#P.creation_deck()
#print(P.deck_id)
#print(P.draw(1)[0])
