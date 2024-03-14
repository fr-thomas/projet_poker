import sys
sys.path.append('/home/ensai/Documents/projet_poker')

from DAO.Poker_DAO import Poker_DAO
from business.partie import Partie
from business.joueur import Joueur


class Partie_services():
    """
    Classe fournissant des services pour la gestion d'une partie de poker.
    """
    def __init__(self, partie : Partie):
        """
        Initialise un objet Partie_services avec une instance de Partie.

        Args:
            partie (Partie): L'instance de Partie à gérer.
        """
        self.Partie = partie

    def ajout_pot(self, montant, joueur):
        """
        Ajoute un montant spécifié au pot de la partie et met à jour la mise du joueur.

        Args:
            montant (float): Le montant à ajouter au pot.
            joueur (str): Le nom du joueur ayant misé.
        """
        for j in self.Partie.list_joueur:
            if j.name == joueur:
                   j.pot -= montant
        self.Partie.pot += montant
        self.Partie.mise_max = montant + self.Partie.list_joueur[joueur].mise
        self.Partie.list_joueur[joueur].mise = self.Partie.mise_max
        self.Partie.list_joueur[joueur].premier_tour = False

    def gain_pot(self, joueur):
        """
        Distribue le pot de la partie au(x) joueur(s) gagnant(s).

        Args:
            joueur (str ou list[str]): Le(s) nom(s) du(des) joueur(s) gagnant(s).
        """
        if type(joueur) == str:
            for j in self.Partie.list_joueur:
                if j.name == joueur:
                   j.pot += self.Partie.pot
        elif type(joueur) == list:
            ponderation = len(joueur)
            for j in self.Partie.list_joueur:
                if j.name in joueur:
                   j.pot += self.Partie.pot / ponderation
        self.Partie.pot = 0

    def mise_egale(self):
        """
        Vérifie si tous les joueurs encore en jeu ont misé le même montant après le premier tour de table.

        Returns:
            bool: True si tous les joueurs ont misé le même montant, False sinon.
        """
        for i in range(len(self.Partie.list_joueur)):
             if self.Partie.list_joueur[i].joue_encore is True:
                if self.Partie.list_joueur[i].mise != self.Partie.mise_max or self.Partie.list_joueur[i].premier_tour is True:
                    return False
        return True
