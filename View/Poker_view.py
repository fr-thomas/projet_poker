import sys
sys.path.append('/home/ensai/Documents/projet_poker')

from business.partie import Partie
from business.joueur import Joueur
from DAO.Poker_DAO import Poker_DAO
from Services.Partie_services import Partie_services

class Poker_View():
    """
    Interface utilisateur pour le déroulement d'une partie de poker.
    """
    def __init__(self, partie : Partie):
        """
        Initialise une interface utilisateur pour une partie de poker.

        Args:
            partie (Partie): L'instance de la partie à gérer.
        """
        self.partie = partie

    def manche_un(self):
        """
        Gère la première partie de la manche. De la distribution des cartes au flop.
        """
        Partie = Partie_services(self.partie)
        Poker = Poker_DAO()
        for joueur in self.partie.list_joueur:
            joueur.main = Poker.draw(self.partie.deck_id, 2)
            print(f"{joueur.name} : {joueur.main[0]['value']}{joueur.main[0]['suit']}, {joueur.main[1]['value']}{joueur.main[1]['suit']}")
            print(f"{joueur} a {joueur.pot} jetons")
        self.partie.carte_commune = []
        Partie.ajout_pot(10, self.partie.blind)
        print(f"{self.partie.parle} a misé 10")
        self.partie.next_parle()
        Partie.ajout_pot(20, self.partie.parle)
        print(f"{self.partie.parle} a misé 10")
        self.partie.next_parle()
        while(Partie.mise_egale() is False):
            print(f"La mise est a {self.partie.mise_max}, vous avez {self.partie.list_joueur[self.partie.parle].pot} jetons.")
            choix = input("Choisir suivre, relancer ou coucher: ")
            if choix == "suivre":
                Partie.ajout_pot(self.partie.mise_max - self.partie.list_joueur[self.partie.parle].mise, self.partie.parle)
                print(f"{self.partie.parle} suit et mise à {self.partie.mise_max}")
            if choix == "relancer":
                print("non")
                relance = int(input("Relancer à combien: "))
                Partie.ajout_pot(relance - self.partie.list_joueur[self.partie.parle].mise, self.partie.parle)
                print(f"{self.partie.parle} suit et relance à {self.partie.mise_max}")
            if choix == "coucher":
                self.partie.list_joueur[self.partie.parle].joue_encore = False
                print(f"{self.partie.parle} se couche.")
            self.partie.next_parle()
        if self.partie.en_lice() is True:
            draw = Poker.draw(self.partie.deck_id, 3)
            self.partie.carte_commune += draw
            print(f"River : {self.partie.carte_commune[0]['value']}{self.partie.carte_commune[0]['suit']}, {self.partie.carte_commune[1]['value']}{self.partie.carte_commune[1]['suit']}, {self.partie.carte_commune[2]['value']}{self.partie.carte_commune[2]['suit']}")
            self.manche_deux()
        else:
            Partie.gain_pot(self.partie.en_lice())
            self.partie.next_blind()
            for joueur in self.partie.list_joueur:
                if joueur.pot != 0:
                    joueur.joue_encore = True
                else:
                    joueur.joue_encore = False
            return False

    def manche_deux(self):
        """
        Gère la deuxième partie de la manche. Du flop au turn et du turn à la river.
        """
        Partie = Partie_services(self.partie)
        self.partie.parle = self.partie.blind
        for joueur in self.partie.list_joueur:
            if joueur.pot != 0:
                joueur.joue_encore = True
                joueur.premier_tour = True
        while self.partie.list_joueur[self.partie.parle].joue_encore is False:
            self.partie.next_parle()
        while(Partie.mise_egale() is False):
            print(f"La mise est a {self.partie.mise_max}, vous avez {self.partie.list_joueur[self.partie.parle].pot} jetons.")
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
            draw = Poker.draw(self.partie.deck_id, 1)
            self.partie.carte_commune += draw
            if len(self.partie.carte_commune) == 4:
                print(f"River : {self.partie.carte_commune[0]['value']}{self.partie.carte_commune[0]['suit']}, {self.partie.carte_commune[1]['value']}{self.partie.carte_commune[1]['suit']}, {self.partie.carte_commune[2]['value']}{self.partie.carte_commune[2]['suit']}, {self.partie.carte_commune[3]['value']}{self.partie.carte_commune[3]['suit']}")
                self.manche_deux()
            else:
                print(f"River : {self.partie.carte_commune[0]['value']}{self.partie.carte_commune[0]['suit']}, {self.partie.carte_commune[1]['value']}{self.partie.carte_commune[1]['suit']}, {self.partie.carte_commune[2]['value']}{self.partie.carte_commune[2]['suit']}, {self.partie.carte_commune[3]['value']}{self.partie.carte_commune[3]['suit']}, {self.partie.carte_commune[4]['value']}{self.partie.carte_commune[4]['suit']}")
                self.manche_trois()
        else:
            Partie.gain_pot(self.partie.en_lice())
            self.partie.next_blind()
            for joueur in self.partie.list_joueur:
                if joueur.pot != 0:
                    joueur.joue_encore = True
                else:
                    joueur.joue_encore = False

    def manche_trois(self):
        """
        Gère la troisième manche de la partie. De la river à la fin de manche.
        """
        Partie = Partie_services(self.partie)
        self.partie.parle = self.partie.blind
        for joueur in self.partie.list_joueur:
            if joueur.pot != 0:
                joueur.joue_encore = True
                joueur.premier_tour = True
        while self.partie.list_joueur[self.partie.parle].joue_encore is False:
            self.partie.next_parle()
        while(Partie.mise_egale() is False):
            print(f"La mise est a {self.partie.mise_max}, vous avez {self.partie.list_joueur[self.partie.parle].pot} jetons.")
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

        gagnant = self.partie.better_hand()
        print(f"{gagnant} a la meilleur main et gagne {self.partie.pot} jetons !")
        Partie.gain_pot(gagnant)

        for joueur in self.partie.list_joueur:
            if joueur.pot != 0:
                joueur.joue_encore = True
                print(joueur.name + "True")
            else:
                joueur.joue_encore = False
                print(joueur.name + "False")
        
        if self.partie.en_lice() == 1:
            for joueur in self.partie.list_joueur:
                if joueur.joue_encore is True:
                    gagnant_partie = joueur.name
            print(f"Le gagnat de la partie est {gagnant_partie} !")
        else:
            self.partie.next_blind()
            Poker = Poker_DAO()
            Poker.shuffle(self.partie.deck_id)
            self.manche_un()