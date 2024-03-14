from View.Poker_view import Poker_View
from DAO.Poker_DAO import Poker_DAO
from business.partie import Partie
from business.joueur import Joueur

if __name__ == "__main__":

    Poker_D = Poker_DAO()
    Poker_D.creation_deck()
    list_joueur = [Joueur("Thomas", 100), Joueur("Léna", 100)]
    Partie1 = Partie(Poker_D.deck_id, list_joueur)
    Poker_V = Poker_View(Partie1)
    Poker_V.manche_un()