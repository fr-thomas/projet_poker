import sys
sys.path.append('/home/ensai/Documents/projet_poker')
from business.joueur import Joueur
from itertools import combinations

class Partie():
    """
    Classe représentant une partie de poker.

    Attributes:
        deck_id (str): L'identifiant du jeu de cartes utilisé dans la partie.
        list_joueur (list[Joueur]): La liste des joueurs participant à la partie.
        pot (float): Le montant total du pot de la partie, initialisé à 0.
        blind (int): L'index du joueur actuellement en position de petite blind.
        parle (int): L'index du joueur actuellement en train de jouer.
        mise_max (float): La mise la plus grande dans la manche.
        carte_commune (list): Les cartes commune a tous les joueurs.
    """

    def __init__(self, deck_id, list_joueur : list[Joueur], pot = 0):
        """
        Initialise un objet Partie avec l'identifiant du jeu de cartes, la liste des joueurs et le montant initial du pot.

        Args:
            deck_id (str): L'identifiant du jeu de cartes.
            list_joueur (list[Joueur]): La liste des joueurs participant à la partie.
            pot (float): Le montant initial du pot de la partie (par défaut à 0).
        """
        self.deck_id = deck_id
        self.list_joueur = list_joueur
        self.pot = pot
        self.blind = 0
        self.parle = 0
        self.mise_max = 0
        self.carte_commune = []

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères de l'objet Partie.

        Returns:
            str: Une chaîne de caractères représentant l'objet Partie.
        """
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
        """
        Passe la position de blind au prochain joueur encore en jeu et lui donne la parole.
        """
        index_blind = (self.list_joueur.index(self.blind)+ 1) % len(self.list_joueur)
        while not self.list_joueur[index_blind].joue_encore:
            index_blind = (index_blind + 1) % len(self.list_joueur)
        self.blind = self.list_joueur[index_blind].name
        self.parle = self.list_joueur[index_blind].name

    def next_parle(self):
        """
        Passe la parole au prochain joueur encore en jeu.
        """
        current_index = self.parle
        next_index = (current_index + 1) % len(self.list_joueur)
        while not self.list_joueur[next_index].joue_encore:
            next_index = (next_index + 1) % len(self.list_joueur)
        self.parle = next_index

    def en_lice(self):
        """
        Vérifie s'il reste des joueurs en lice dans la manche, si il n'en reste qu'un on récuperer son pseudo.

        Returns:
            Union[bool, str]: Le nom du joueur gagnant s'il est seul en lice, True sinon.
        """
        compteur = 0
        for joueur in self.list_joueur:
            if joueur.joue_encore is True:
                compteur += 1
        if compteur == 1:
            for joueur in self.list_joueur:
                if joueur.joue_encore is True:
                    return joueur.name
        return True

    def better_hand_alone(self, main):
        """
        Évalue la force d'une main de 5 cartes.

        Args:
            main (list): La main de cartes à évaluer.

        Returns:
            list: Une liste contenant le score de la main.
        """
        valeurs = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'JACK': 11, 'QUEEN': 12, 'KING': 13, 'ACE': 14}
        valeurs_main = sorted([valeurs[carte['value']] for carte in main], reverse=True)
        couleurs_main = [carte['suit'] for carte in main]
        
        # Cas ou l'as vaut 1
        if valeurs_main == [14, 5, 4, 3, 2]:
            valeurs_main = [1, 5, 4, 3, 2]

        # Quinte flush
        if len(set(couleurs_main)) == 1 and max(valeurs_main) - min(valeurs_main) == 4:
            return [10, max(valeurs_main)]

        # Carré
        for valeur in valeurs_main:
            if valeurs_main.count(valeur) == 4:
                return [9, valeur] + [c for c in valeurs_main if c != valeur]

        # Full
        triplet = None
        paire = None
        for valeur in valeurs_main:
            if valeurs_main.count(valeur) == 3:
                triplet = valeur
            elif valeurs_main.count(valeur) == 2:
                paire = valeur
        if triplet is not None and paire is not None:
            return [7, triplet, paire]

        # Couleur
        if len(set(couleurs_main)) == 1:
            return [6] + sorted(valeurs_main, reverse=True)

        # On vérifie la quinte plus tard

        # Brelan
        for valeur in valeurs_main:
            if valeurs_main.count(valeur) == 3:
                return [4, valeur] + sorted([c for c in valeurs_main if c != valeur], reverse=True)

        # Double paire
        paires = set()
        for valeur in valeurs_main:
            if valeurs_main.count(valeur) == 2:
                paires.add(valeur)
        if len(paires) == 2:
            return [3, max(paires), min(paires)] + [c for c in valeurs_main if c not in paires]

        # Paire
        for valeur in valeurs_main:
            if valeurs_main.count(valeur) == 2:
                return [2, valeur] + sorted([c for c in valeurs_main if c != valeur], reverse=True)

        # On vérifie la quint en étant sur qu'il n'y a pas de paire, de brelan ou de carré
        if max(valeurs_main) - min(valeurs_main) == 4:
            return [5, max(valeurs_main)]

        # Sinon, la main a une carte haute
        return [1] + sorted([c for c in valeurs_main], reverse=True)

    def better_hand(self):
        """
        Détermine le(s) joueur(s) avec la meilleure main parmi les joueurs encore en lice.

        Returns:
            Union[str, List[str]]: Le nom du joueur gagnant s'il est seul, une liste de noms de joueurs en cas d'égalité.
        """
        meilleur_main = {}
        for joueur in self.list_joueur:
            meilleures_evaluation = None
            combinaisons = combinations(joueur.main + self.carte_commune, 5)

            for combinaison in combinaisons:
                evaluation = self.better_hand_alone(combinaison)
                if meilleures_evaluation is None:
                    meilleures_evaluation = evaluation
                if evaluation != meilleures_evaluation:
                    for i in range(len(evaluation)):
                        if evaluation[i] > meilleures_evaluation[i]:
                            meilleures_evaluation = evaluation
                        elif evaluation[i] < meilleures_evaluation[i]:
                            break

            meilleur_main[joueur.name] = meilleures_evaluation
        print(meilleur_main)
        score_max = max(meilleur_main[joueur][0] for joueur in meilleur_main)
        joueurs_max_score = [joueur for joueur in meilleur_main if meilleur_main[joueur][0] == score_max]
        print(score_max)
        print(joueurs_max_score)

        if len(joueurs_max_score) == 1:
               return joueurs_max_score[0]

        score = None
        Tie = False
        for joueur in joueurs_max_score:
            if score is None:
                score = meilleur_main[joueur]
            elif meilleur_main[joueur] != score:
                Tie = False
                break
            else:
                Tie = True
        if Tie is True :
            return joueurs_max_score

        for i in range(1, len(meilleur_main[joueurs_max_score[0]])):
            if len(joueurs_max_score) == 1:
               return joueurs_max_score[0]

            score_max = max(meilleur_main[joueur][i] for joueur in joueurs_max_score)
            joueurs_max_score = [joueur for joueur in joueurs_max_score if meilleur_main[joueur][i] == score_max]
