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

        self.name = name
        self.pot = pot

    ####################################
    #             Methods              #
    ####################################
    def __str__(self):
        return (
            f"name: {self.name}, "
            f"pot: {self.pot}, "
        )