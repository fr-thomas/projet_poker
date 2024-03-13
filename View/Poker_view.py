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
        "Du début au flop"
        Partie = Partie_services(self.partie)
        Partie.ajout_pot(10, self.partie.blind)
        self.partie.next_parle()
        Partie.ajout_pot(20, self.partie.parle)
        self.partie.next_parle()
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
            self.partie.next_blind()
            for joueur in self.partie.list_joueur:
                if joueur.pot != 0:
                    joueur.joue_encore = True
                else:
                    joueur.joue_encore = False
    
    def manche_deux(self):
        "Represente du flop au turn et du turn à la river"
        Partie = Partie_services(self.partie)
        self.partie.parle = self.partie.blind
        while self.partie.list_joueur[self.partie.parle].joue_encore is False:
            self.partie.next_parle()
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
            draw = Poker.draw(1)
            self.partie.carte_commune + draw["cards"]
        else:
            Partie.gain_pot(self.partie.en_lice())
            self.partie.next_blind()
            for joueur in self.partie.list_joueur:
                if joueur.pot != 0:
                    joueur.joue_encore = True
                else:
                    joueur.joue_encore = False
    
    def manche_trois(self):
        "Représente la river à la fin"
        Partie = Partie_services(self.partie)
        Partie.ajout_pot(10, self.partie.parle)
        self.partie.next_parle()
        Partie.ajout_pot(20, self.partie.parle)
        self.partie.next_parle()
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
            gagnant = self.partie.better_hand()
            Partie.gain_pot(self.partie.en_lice())
        else:
            Partie.gain_pot(self.partie.en_lice())
            self.partie.next_blind()
            for joueur in self.partie.list_joueur:
                if joueur.pot != 0:
                    joueur.joue_encore = True
                else:
                    joueur.joue_encore = False