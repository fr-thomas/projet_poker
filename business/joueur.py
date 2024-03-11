class Joueur():

    ####################################
    #           Constructor            #
    ####################################

    def __init__(
        self,
        name,
        pot
    ) -> None:

        ####################################
        #           Attributes             #
        ####################################

        self._name = name
        self._pot = pot

    ####################################
    #             Methods              #
    ####################################
    def __str__(self):
        return (
            f"name: {self._name}, "
            f"pot: {self._pot}, "
        )