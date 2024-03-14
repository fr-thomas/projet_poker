import requests


class Poker_DAO():
    """
    Cette classe fournit des fonctionnalités pour interagir avec un jeu de cartes à l'aide de l'API Deck of Cards (https://deckofcardsapi.com/).
    
    Attributs:
        deck_id (str): L'identifiant unique du jeu de cartes.

    Méthodes:
        __init__(): Initialise l'objet Poker_DAO

        creation_deck(): Crée un nouveau jeu de cartes et assigne son identifiant unique à self.deck_id.

        draw(deck_id, nbr_carte): Tire un nombre spécifié de cartes du jeu identifié par deck_id.

        shuffle(deck_id): Mélange le jeu identifié par deck_id.
    """
    def __init__(self):
        """
        Initialise un objet Poker_DAO
        """
        self.deck_id = None

    def creation_deck(self):
        """
        Crée un nouveau jeu de cartes à l'aide de l'API Deck of Cards et assigne son identifiant unique à self.deck_id.
        """
        response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/")
        deck = response.json()
        self.deck_id = deck["deck_id"]

    def draw(self, deck_id, nbr_carte):
        """
        Tire un nombre spécifié de cartes du jeu identifié par deck_id.

        Args:
            deck_id (str): L'identifiant unique du jeu de cartes.
            nbr_carte (int): Le nombre de cartes à tirer du jeu.

        Returns:
            list: Une liste contenant des informations sur les cartes tirées.
        """
        response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={nbr_carte}")
        tirage = response.json()
        return tirage["cards"]

    def shuffle(self, deck_id):
        """
        Mélange le jeu identifié par deck_id en utilisant l'API Deck of Cards.

        Args:
            deck_id (str): L'identifiant unique du jeu de cartes.
        """
        requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/shuffle/")
