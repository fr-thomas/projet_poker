class Joueur():

    ####################################
    #           Constructor            #
    ####################################

    def __init__(
        self,
        name,
        pot,
    ) -> None:

        ####################################
        #           Attributes             #
        ####################################

        self.name = name
        self.pot = pot
        self.main = None
        self.mise = 0
        self.joue_encore = True

    ####################################
    #             Methods              #
    ####################################
    def __str__(self):
        return (
            f"name: {self.name}, "
            f"pot: {self.pot}, "
            f"main: {self.main}, "
            f"mise: {self.mise}, "
            f"joue_encore: {self.joue_encore}, "
        )