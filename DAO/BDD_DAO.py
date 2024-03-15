import sqlite3
import json

class BDD_DAO:
    """
    Classe pour gérer l'accès à une base de données SQLite pour le jeu de poker.
    """
    def __init__(self):
        """
        Initialise une instance de BDD_DAO et établit la connexion à la base de données.
        """
        self.conn = sqlite3.connect("/home/ensai/Documents/projet_poker/data/partie.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def save_partie(self, partie):
        """
        Sauvegarde une partie de poker dans la base de données.

        Args:
            partie (Partie): L'objet Partie à sauvegarder.
        """
        self.cursor.execute('''INSERT INTO parties (deck_id, joueurs, pot, blind, parle, mise_max, carte_commune)
                               VALUES (?, ?, ?, ?, ?, ?, ?)''',
                            (partie.deck_id, json.dumps(partie.list_joueur), partie.pot, partie.blind, partie.parle, partie.mise_max, json.dumps(partie.carte_commune)))
        self.conn.commit()

    def load_parties(self):
        """
        Charge toutes les parties enregistrées depuis la base de données.

        Returns:
            list: Une liste contenant les données de toutes les parties chargées.
        """
        self.cursor.execute('''SELECT * FROM parties''')
        rows = self.cursor.fetchall()
        parties = []
        for row in rows:
            partie = {
                'deck_id': row[1],
                'joueurs': json.loads(row[2]),
                'pot': row[3],
                'blind': row[4],
                'parle': row[5],
                'mise_max': row[6],
                'carte_commune': json.loads(row[7])
            }
            parties.append(partie)
        return parties

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        self.conn.close()