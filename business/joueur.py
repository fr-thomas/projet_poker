class Joueur():
    """
    Classe représentant un joueur dans un jeu de poker.

    Attributes:
        name (str): Le nom du joueur.
        pot (float): Le montant d'argent disponible pour le joueur.
        main (list): La main du joueur, initialisée à None.
        mise (float): Le montant misé par le joueur, initialisé à 0.
        joue_encore (bool): Indique si le joueur joue encore dans la manche en cours, initialisé à True.
        premier_tour (bool): Indique si c'est le premier tour de jeu pour le joueur, initialisé à True.
    """

    def __init__(self, name):
        """
        Initialise un objet Joueur avec le nom et le montant initial du pot du joueur.

        Args:
            name (str): Le nom du joueur.
            pot (float): Le montant initial d'argent pour le joueur.
        """
        self.name = name
        self.pot = 500
        self.main = None
        self.mise = 0
        self.joue_encore = True
        self.premier_tour = True

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères de l'objet Joueur.

        Returns:
            str: Une chaîne de caractères représentant l'objet Joueur.
        """
        return (
            f"name: {self.name}, "
            f"pot: {self.pot}, "
            f"main: {self.main}, "
            f"mise: {self.mise}, "
            f"joue_encore: {self.joue_encore}, "
        )
    