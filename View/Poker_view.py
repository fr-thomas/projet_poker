import sys
sys.path.append('/home/ensai/Documents/projet_poker')

from business.partie import Partie
from business.joueur import Joueur
from DAO.Poker_DAO import Poker_DAO
from Services.Partie_services import Partie_services

class Poker_View():
    """
    """
    def __init__(self, nbr_joueur, list_nom, pot_indiv, pot_depart = 0) -> None:
        Poker = Poker_DAO()
        Poker.creation_deck()
        list_joueur = []
        for i in range(nbr_joueur):
            list_joueur.append(Joueur(list_nom[i], pot_indiv))
        self.partie = Partie(Poker.deck_id, list_joueur, pot_depart)

    def manche_un(self):
        Partie = Partie_services(self.partie)
        Partie.ajout_pot(10, self.partie.blind)
        self.partie.next_parle()
        Partie.ajout_pot(20, self.partie.parle)
        while(Partie.mise_egale() is False):
            choix = input("Choisir suivre, relancer ou coucher: ")
            if choix == "suivre":
                Partie.ajout_pot(self.partie.mise_max - self.partie.list_joueur[self.partie.parle].mise, self.partie.parle)
            if choix == "relancer":
                relance = input("Relancer à combien: ")
                Partie.ajout_pot(relance - self.partie.list_joueur[self.partie.parle].mise, self.partie.parle)
                self.partie.list_joueur[self.partie.parle].mise = relance
            if choix == "coucher":
                self.partie.list_joueur[self.partie.parle].joue_encore = False
            self.partie.next_parle()
        if self.partie.en_lice() is True:
            Poker = Poker_DAO()
            draw = Poker.draw(3)
            self.partie.carte_commune + draw["cards"]
        else:
            Partie.gain_pot(self.partie.en_lice())
    
    def manche_deux(self):
        Partie = Partie_services(self.partie)
        Partie.ajout_pot(10, self.partie.parle)
        self.partie.next_parle()
        Partie.ajout_pot(20, self.partie.parle)
        while(Partie.mise_egale() is False):
            choix = input("Choisir suivre, relancer ou coucher: ")
            if choix == "suivre":
                Partie.ajout_pot(self.partie.mise_max - self.partie.list_joueur[self.partie.parle].mise, self.partie.parle)
            if choix == "relancer":
                relance = input("Relancer à combien: ")
                Partie.ajout_pot(relance - self.partie.list_joueur[self.partie.parle].mise, self.partie.parle)
                self.partie.list_joueur[self.partie.parle].mise = relance
            if choix == "coucher":
                self.partie.list_joueur[self.partie.parle].joue_encore = False
            self.partie.next_parle()
        if self.partie.en_lice() is True:
            Poker = Poker_DAO()
            draw = Poker.draw(3)
            self.partie.carte_commune + draw["cards"]
        else:
            Partie.gain_pot(self.partie.en_lice())