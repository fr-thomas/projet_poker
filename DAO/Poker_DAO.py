import requests


class Poker():
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

    def draw(self, nbr_carte):
        """
        Tirer 1-2 carte(s)
        """
        response = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count={nbr_carte}")
        tirage = response.json()
        return tirage["cards"]


P = Poker()
P.creation_deck()
print(P.deck_id)
print(P.draw(2)[1])
