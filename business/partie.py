import sys
sys.path.append('/home/ensai/Documents/projet_poker')
from business.joueur import Joueur


class Partie():

    ####################################
    #           Constructor            #
    ####################################

    def __init__(
        self,
        deck_id,
        list_joueur : list[Joueur],
        pot = 0,
    ) -> None:

        ####################################
        #           Attributes             #
        ####################################

        self.deck_id = deck_id
        self.list_joueur = list_joueur
        self.pot = pot
        self.blind = list_joueur[0].name
        self.parle = list_joueur[0].name
        self.mise_max = 0
        self.carte_commune = []

    ####################################
    #             Methods              #
    ####################################
    def __str__(self):
        return (
            f"deck_id: {self.deck_id}, "
            f"list_joueur: {self.list_joueur}, "
            f"pot: {self.pot}, "
            f"blind: {self.blind}, "
            f"parle: {self.parle}, "
            f"mise_max: {self.mise_max}, "
            f"carte_commune: {self.carte_commune}, "
        )

    def next_blind(self):
        global index_blind
        index_blind = (index_blind + 1) % len(self.list_joueur)
        if self.list_joueur[index_blind].joue_encore is False:
            self.next_blind()
        else:
            self.blind = self.list_joueur[index_blind].name


    def next_parle(self):
        global index_parle
        index_parle = (index_parle + 1) % len(self.list_joueur)
        if self.list_joueur[index_parle].joue_encore is False:
            self.next_parle()
        else:
            self.parle = self.list_joueur[index_parle].name

    def en_lice(self):
        compteur = 0
        for joueur in self.list_joueur:
            if joueur.joue_encore is True:
                compteur += 1
        if compteur == 1:
            for joueur in self.list_joueur:
                if joueur.joue_encore is True:
                    return joueur.name
        return True