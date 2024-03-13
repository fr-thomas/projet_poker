import sys
sys.path.append('/home/ensai/Documents/projet_poker')

from DAO.Poker_DAO import Poker_DAO
from business.partie import Partie
from business.joueur import Joueur


class Partie_services():
    """
    """
    def __init__(self, partie : Partie):
        self.Partie = partie

    def ajout_pot(self, montant, joueur):
        """
        """
        for j in self.Partie.list_joueur:
            if j.name == joueur:
                   j.pot -= montant
        self.Partie.pot += montant
    
    def gain_pot(self, joueur):
        for j in self.joueurs:
            if j.name == joueur:
                   j.pot += self.Partie.pot
        self.Partie.pot = 0

    def distribution(self):
        for joueur in self.joueurs:
            joueur.main = self.deck.draw(2)

    def mise_egal(self):
        """
        Verifie l'egalité de mise de chaque joueur encore en jeux
        """
        for i in range(len(self.Partie.list_joueur)):
             if self.Partie.list_joueur[i].joue_encore is True:
                if self.Partie.list_joueur[i].mise != self.Partie.mise_max:
                    return False
        return True


#P=Partie_services(3456,3,[Joueur("Alice",3),Joueur("Bob",0),Joueur("Martin",10)])
#print(P.Partie.pot)
#print(P.joueurs[1])
#print(P.joueurs[0])
#P.ajout_pot(10)
#P.gain_pot("Bob")
#print(P.Partie.pot)
#print(P.joueurs[1])
#print(P.joueurs[0])
