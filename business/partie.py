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

        self._deck_id = deck_id
        self._pot = nbr_joueur

    ####################################
    #             Methods              #
    ####################################
    def __str__(self):
        return (
            f"name: {self._name}, "
            f"pot: {self._pot}, "
        )