import sys
sys.path.append('/home/ensai/Documents/projet_poker')

from DAO.Poker_DAO import Poker_DAO
from business.partie import Partie
from business.joueur import Joueur


class Partie_services():
    """
    """
    def __init__(self, deck_id, nbr_joueur, joueurs: list[Joueur]):
        self.Partie = Partie(deck_id,nbr_joueur)
        self.joueurs = joueurs

    def ajout_pot(self, montant):
        """
        """
        self.Partie.pot += montant
    
    def gain_pot(self, joueur):
        for joueur in self.joueurs:
            joueur.pot += self.Partie.pot
        self.Partie.pot = 0


P=Partie_services(3456,3,[Joueur("Alice",3),Joueur("Bob",0),Joueur("Martin",10)])
print(P.joueurs)
P.ajout_pot(10)
P.gain_pot("Bob")
print(P.Partie.pot)
print(P.joueurs[1])
