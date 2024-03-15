import sys
sys.path.append('/home/ensai/Documents/projet_poker')

import tkinter as tk
from tkinter import messagebox

from business.partie import Partie
from business.joueur import Joueur
from DAO.Poker_DAO import Poker_DAO
from Services.Partie_services import Partie_services
from View.Poker_view import Poker_View

class Start_View():
    """
    Interface utilisateur pour démarrer une nouvelle partie de poker.

    Attributes:
        master (tk.Tk): La fenêtre principale de l'application.
        label (tk.Label): Libellé pour accueillir l'utilisateur.
        load_button (tk.Button): Bouton pour charger une partie existante.
        new_button (tk.Button): Bouton pour créer une nouvelle partie.
        player_label (tk.Label): Libellé pour sélectionner le nombre de joueurs.
        player_options (tk.Listbox): Liste déroulante pour choisir le nombre de joueurs.
        new_window (tk.Toplevel): Fenêtre pour saisir les noms des joueurs lors de la création d'une nouvelle partie.
        player_entries (list): Liste des champs de saisie des noms des joueurs.
    """
    def __init__(self, master):
        """
        Initialise une interface utilisateur pour démarrer une nouvelle partie de poker.

        Args:
            master (tk.Tk): La fenêtre principale de l'application.
        """
        self.master = master
        self.master.title("Poker")
        self.master.geometry("1000x800")

        self.label = tk.Label(master, text="Bienvenue sur cette application de poker.\nChoisissez votre partie:")
        self.label.pack()

        self.load_button = tk.Button(master, text="Charger une partie existante", command=self.load_game)
        self.load_button.place(x=200, y=350)

        self.new_button = tk.Button(master, text="Créer une nouvelle partie", command=self.new_game)
        self.new_button.place(x=650, y=350)

        self.player_label = tk.Label(master, text="Nombre de joueurs:")
        self.player_label.place(x=650, y=400)
        self.player_options = tk.Listbox(master, selectmode=tk.SINGLE, height=7)
        for i in range(2, 7):
            self.player_options.insert(tk.END, i)
        self.player_options.selection_set(0)
        self.player_options.place(x=650, y=420)


    def load_game(self):
        """
        Est sensé chargé une partie depuis la BDD mais je n'ai pas eu le temps.
        """
        messagebox.showinfo("Charger une partie", "Fonctionnalité non implémentée")

    def new_game(self):
        """
        Lance la création d'une nouvelle partie en fonction du nombre de joueurs sélectionné.
        """
        selected_players = self.player_options.curselection()
        num_players = int(self.player_options.get(selected_players[0]))

        window_height = 60 + num_players * 30
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Nouvelle partie")
        self.new_window.geometry(f"400x{window_height}")

        self.player_entries = []
        for i in range(num_players):
            label = tk.Label(self.new_window, text=f"Joueur {i+1}:")
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(self.new_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.player_entries.append(entry)

        start_button = tk.Button(self.new_window, text="Commencer", command=self.start_game)
        start_button.grid(row=num_players, columnspan=2, pady=10)

    def start_game(self):
        """
        Démarre une nouvelle partie de poker avec les noms des joueurs saisis.
        Affiche une erreur si les noms des joueurs sont vides ou identiques.
        """
        player_names = [entry.get().strip() for entry in self.player_entries]
        if all(player_names) and len(set(player_names)) == len(player_names):
            self.new_window.destroy()
            liste_joueur = []
            for joueur in player_names:
                liste_joueur.append(Joueur(joueur))
            Poker = Poker_DAO()
            Poker.creation_deck()
            Jeux = Poker_View(self.master, Partie(Poker.deck_id, liste_joueur))
            Jeux.manche_un()
        else:
            messagebox.showerror("Erreur", "Veuillez saisir des noms de joueurs différents et non vides.")
