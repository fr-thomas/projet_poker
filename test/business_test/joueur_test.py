import sys
sys.path.append('/home/ensai/Documents/projet_poker')
import unittest
from business.joueur import Joueur
from business.partie import Partie

class TestPartie(unittest.TestCase):

    def setUp(self):
        joueur1 = Joueur("Joueur 1")
        joueur2 = Joueur("Joueur 2")
        joueur3 = Joueur("Joueur 3")
        self.partie = Partie("deck_id", [joueur1, joueur2, joueur3])

    def test_init(self):
        self.assertEqual(self.partie.deck_id, "deck_id")
        self.assertEqual(len(self.partie.list_joueur), 3)
        self.assertEqual(self.partie.pot, 0)
        self.assertEqual(self.partie.blind, self.partie.list_joueur[0])
        self.assertEqual(self.partie.parle, self.partie.list_joueur[0])
        self.assertEqual(self.partie.mise_max, 0)
        self.assertEqual(self.partie.carte_commune, [])

    def test_next_blind(self):
        self.partie.next_blind()
        self.assertEqual(self.partie.blind, self.partie.list_joueur[1])
        self.assertEqual(self.partie.parle, self.partie.list_joueur[1])

    def test_next_parle(self):
        self.partie.next_parle()
        self.assertEqual(self.partie.parle, self.partie.list_joueur[1])

    def test_en_lice(self):
        self.partie.list_joueur[0].joue_encore = False
        self.partie.list_joueur[1].joue_encore = True
        self.partie.list_joueur[2].joue_encore = True
        self.assertTrue(self.partie.en_lice())
        self.partie.list_joueur[1].joue_encore = False
        self.assertTrue(self.partie.en_lice() == "Joueur 3")

    def test_better_hand(self):
        joueur1 = Joueur("Joueur 1")
        joueur2 = Joueur("Joueur 2")
        partie = Partie("deck_id", [joueur1, joueur2])
        main_joueur1 = [
            {'value': '2', 'suit': 'HEARTS'},
            {'value': '2', 'suit': 'CLUBS'},
        ]
        main_joueur2 = [
            {'value': 'QUEEN', 'suit': 'HEARTS'},
            {'value': 'ACE', 'suit': 'HEARTS'},
        ]
        carte_commune = [
            {'value': '6', 'suit': 'HEARTS'},
            {'value': 'JACK', 'suit': 'HEARTS'},
            {'value': 'KING', 'suit': 'HEARTS'},
            {'value': '2', 'suit': 'SPADES'},
            {'value': '10', 'suit': 'HEARTS'}
        ]
        partie.list_joueur[0].main = main_joueur1
        partie.list_joueur[1].main = main_joueur2
        partie.carte_commune = carte_commune

        self.assertEqual(partie.better_hand(), 'Joueur 2')

if __name__ == '__main__':
    unittest.main()