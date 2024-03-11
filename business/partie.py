from business.joueur import Joueur


class Partie():

    ####################################
    #           Constructor            #
    ####################################

    def __init__(
        self,
        deck_id,
        nbr_joueur
    ) -> None:

        ####################################
        #           Attributes             #
        ####################################

        self.deck_id = deck_id
        self.nbr_joueure = nbr_joueur
        self.pot = 0

    ####################################
    #             Methods              #
    ####################################
    def __str__(self):
        return (
            f"name: {self.name}, "
            f"pot: {self.pot}, "
        )