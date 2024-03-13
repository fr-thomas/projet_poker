import sys
sys.path.append('/home/ensai/Documents/projet_poker')
from business.joueur import Joueur
from itertools import combinations

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

    def better_hand_alone(self, main):
        """
        retourne le score d'une main de 5 cartes
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

        # Quinte
        if max(valeurs_main) - min(valeurs_main) == 4:
            return [5, max(valeurs_main)]

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

        # Sinon, la main a une carte haute
        return [1] + sorted([c for c in valeurs_main], reverse=True)

    def better_hand(self):
        """
        """
        meilleur_main = {}
        for joueur in self.list_joueur:
            meilleures_evaluation = None
            combinaisons = combinations(joueur.main + self.carte_commune, 5)

            for combinaison in combinaisons:
                evaluation = self.better_hand_alone(combinaison)
                if evaluation != meilleures_evaluation:
                    for i in range(len(evaluation)):
                        if evaluation[i] > meilleures_evaluation[i]:
                            meilleures_evaluation = evaluation
                        elif evaluation[i] < meilleures_evaluation[i]:
                            break

            meilleur_main[joueur.name] = meilleures_evaluation

        score_max = max(meilleur_main[joueur][0] for joueur in meilleur_main)
        joueurs_max_score = [joueur for joueur in meilleur_main if meilleur_main[joueur][0] == score_max]

        for i in range(1, len(meilleur_main[joueurs_max_score[0]])):
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

            score_max = max(meilleur_main[joueur][i] for joueur in joueurs_max_score)
            joueurs_max_score = [joueur for joueur in joueurs_max_score if meilleur_main[joueur][i] == score_max]