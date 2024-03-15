import sys
sys.path.append('/home/ensai/Documents/projet_poker')

import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

from business.partie import Partie
from business.joueur import Joueur
from DAO.Poker_DAO import Poker_DAO
from Services.Partie_services import Partie_services

class Poker_View():
    """
    Interface utilisateur pour le déroulement d'une partie de poker.
    """
    def __init__(self, master, partie : Partie):
        """
        Initialise une interface utilisateur pour une partie de poker.

        Args:
            master (tk.Tk): La fenêtre principale de l'application.
            partie (Partie): L'instance de la partie à gérer.
        """
        self.partie = partie
        self.master = master

        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.title("Poker")
        window_height = 100 + len(self.partie.list_joueur) * 300
        self.master.geometry(f"1000x{window_height}")

        self.label = tk.Label(self.master, text="Début de partie")
        self.label.place(x=700, y=200)

        self.label_joueur = []
        self.carte = []
        self.show_carte = []
        self.buttons_suivre = []
        self.buttons_relancer = []
        self.buttons_coucher = []
        self.relance = []

        for i, joueur in enumerate(self.partie.list_joueur):
            self.label_joueur.append(tk.Label(master, text=f"{joueur.name} \n ({joueur.pot} jetons)"))
            self.label_joueur[i].place(x= 40 , y=120*(i+1)-40)

            self.show_carte.append(False)
            self.carte.append(tk.Button(self.master, text="Carte", command=lambda i=i, joueur=joueur: self.voir_main(i, joueur)))
            self.carte[i].place(x= 50 , y=120*(i+1) + 15)

            self.buttons_suivre.append(tk.Button(self.master, text="Suivre", command=lambda joueur=joueur: self.suivre(joueur.name)))
            self.buttons_suivre[i].place(x= 150 , y=120*(i+1) + 15)

            self.buttons_relancer.append(tk.Button(self.master, text="Relancer", command=lambda i=i, joueur=joueur: self.relancer(i, joueur)))
            self.buttons_relancer[i].place(x= 250 , y=120*(i+1) + 15)

            self.relance.append(tk.Entry(self.master, width= 5))
            self.relance[i].place(x=250, y=120*(i+1) + 50)

            self.buttons_coucher.append(tk.Button(self.master, text="Se coucher", command=lambda joueur=joueur: self.coucher(joueur.name)))
            self.buttons_coucher[i].place(x= 350 , y=120*(i+1) + 15)

    def suivre(self, joueur):
        """
        Gère l'action de suivre pour un joueur.

        Args:
            joueur (str): Le nom du joueur qui suit.
        """
        if joueur == self.partie.parle.name:
            for i, j in enumerate(self.partie.list_joueur):
                if j.name == joueur:
                    Partie = Partie_services(self.partie)
                    Partie.ajout_pot(self.partie.mise_max - j.mise, joueur)
                    self.partie.next_parle()
                    self.label_joueur[i].destroy()
                    self.label_joueur[i] = tk.Label(self.master, text=f"{j.name} \n ({j.pot} jetons)")
                    self.label_joueur[i].place(x= 40 , y=120*(i+1)-40)
                    self.label.destroy()
                    self.label = tk.Label(self.master, text=f"{joueur} suit à {self.partie.mise_max} jetons")
                    self.label.place(x=700, y=200)
                    if Partie.mise_egale() is True:
                        if len(self.partie.carte_commune) == 0:
                            self.fin_de_manche(3)
                        if len(self.partie.carte_commune) == 3 or len(self.partie.carte_commune) == 4:
                            self.fin_de_manche(1)
                        if len(self.partie.carte_commune) == 5:
                            self.fin_de_manche(0)

    def relancer(self, i, joueur):
        """
        Gère l'action de relance pour un joueur.

        Args:
            i (int): L'index du joueur dans la liste.
            joueur (Joueur): L'instance du joueur qui relance.
        """
        if joueur.name == self.partie.parle.name:
            if int(self.relance[i].get()) < self.partie.mise_max:
                messagebox.showerror("Erreur", f"Veuillez saisir une relance supérieur à la dernière mise : {self.partie.mise_max}.")
            else:
                for j in self.partie.list_joueur:
                    if j.name == joueur.name:
                        Partie = Partie_services(self.partie)
                        Partie.ajout_pot(int(self.relance[i].get()) - j.mise, self.partie.parle.name)
                        self.partie.next_parle()
                        self.label_joueur[i].destroy()
                        self.label_joueur[i] = tk.Label(self.master, text=f"{j.name} \n ({j.pot} jetons)")
                        self.label_joueur[i].place(x= 40 , y=120*(i+1)-40)
                        self.label.destroy()
                        self.label = tk.Label(self.master, text=f"{j.name} relance à {self.partie.mise_max} jetons")
                        self.label.place(x=700, y=200)

                if Partie.mise_egale() is True:
                    if len(self.partie.carte_commune) == 0:
                        self.fin_de_manche(3)
                    if len(self.partie.carte_commune) == 3 or len(self.partie.carte_commune) == 4:
                        self.fin_de_manche(1)
                    if len(self.partie.carte_commune) == 5:
                        self.fin_de_manche(0)

    def coucher(self, joueur):
        """
        Gère l'action de se coucher pour un joueur.

        Args:
            joueur (str): Le nom du joueur qui se couche.
        """
        if joueur == self.partie.parle.name:
            for j in self.partie.list_joueur:
                    if j.name == joueur:
                        j.joue_encore = False
                        j.premier_tour = False
                        self.partie.next_parle()
                        self.label.destroy()
                        self.label = tk.Label(self.master, text=f"{j.name} se couche")
                        self.label.place(x=700, y=200)

                        Partie = Partie_services(self.partie)
                        if Partie.mise_egale() is True:
                            if len(self.partie.carte_commune) == 0:
                                self.fin_de_manche(3)
                            if len(self.partie.carte_commune) == 3 or len(self.partie.carte_commune) == 4:
                                self.fin_de_manche(1)
                            if len(self.partie.carte_commune) == 5:
                                self.fin_de_manche(0)

    def voir_main(self, i, joueur:Joueur):
        """
        Affiche / Cache les cartes d'un joueur.

        Args:
            i (int): L'index du joueur dans la liste.
            joueur (Joueur): L'instance du joueur dont les cartes doivent être affichées.
        """
        if self.show_carte[i] is False:
            carte1 = joueur.main[0]
            carte2 = joueur.main[1]
            request1 = requests.get(carte1["image"])
            request2 = requests.get(carte2["image"])
            self.show_carte[i] = True
        else:
            request1 = requests.get("https://deckofcardsapi.com/static/img/back.png")
            request2 = requests.get("https://deckofcardsapi.com/static/img/back.png")
            self.show_carte[i] = False

        image_data1 = BytesIO(request1.content)
        image_carte1 = Image.open(image_data1)
        image_data2 = BytesIO(request2.content)
        image_carte2 = Image.open(image_data2)

        largeur_miniature = 50
        hauteur_miniature1 = int(largeur_miniature * image_carte1.height / image_carte1.width)
        hauteur_miniature2 = int(largeur_miniature * image_carte2.height / image_carte2.width)
        image_carte1 = image_carte1.resize((largeur_miniature, hauteur_miniature1), Image.ANTIALIAS)
        image_carte2 = image_carte2.resize((largeur_miniature, hauteur_miniature2), Image.ANTIALIAS)
        photo1 = ImageTk.PhotoImage(image_carte1)
        photo2 = ImageTk.PhotoImage(image_carte2)

        label1 = tk.Label(self.master, image=photo1)
        label2 = tk.Label(self.master, image=photo2)
        label1.image = photo1
        label1.place(x=130, y=55 + 120*i)
        label2.image = photo2
        label2.place(x=180, y=55 + 120*i)

    def fin_de_manche(self, nbr_carte):
        """
        Gère ce qu'il se passe après le flop, le turn et la river. (Quand les joueurs voient les cartes communes)

        Args:
            nbr_carte (int): Le nombre de cartes à afficher à la table.
        """
        if nbr_carte == 0:
            gagnant = self.partie.better_hand()
            self.label.destroy()
            self.label = tk.Label(self.master, text=f"{gagnant} gagne la manche et {self.partie.pot} jetons")
            self.label.place(x=700, y=200)
            Partie = Partie_services(self.partie)
            Partie.gain_pot(gagnant)
            self.label1.destroy()
            self.label2.destroy()
            self.label3.destroy()
            self.label4.destroy()
            self.label5.destroy()

            for joueur in self.partie.list_joueur:
                if joueur.pot != 0:
                    joueur.joue_encore = True
                else:
                    joueur.joue_encore = False

            if self.partie.en_lice() == 1:
                for joueur in self.partie.list_joueur:
                    if joueur.joue_encore is True:
                        gagnant_partie = joueur.name
                self.label.destroy
                self.label = tk.Label(self.master, text=f"Le gagant de la partie est {gagnant_partie}")
                self.label.place(x=700, y=200)
                #rajouter un retour au startview
            else:
                self.partie.next_blind()
                Poker = Poker_DAO()
                Poker.shuffle(self.partie.deck_id)
                self.manche_un()

        Partie = Partie_services(self.partie)
        Poker = Poker_DAO()
        if self.partie.en_lice() is True:
            draw = Poker.draw(self.partie.deck_id, nbr_carte)
            self.partie.carte_commune += draw

            if len(self.partie.carte_commune) == 3:
                print("oui")
                request1 = requests.get(self.partie.carte_commune[0]["image"])
                request2 = requests.get(self.partie.carte_commune[1]["image"])
                request3 = requests.get(self.partie.carte_commune[2]["image"])

                image_data1 = BytesIO(request1.content)
                image_carte1 = Image.open(image_data1)
                image_data2 = BytesIO(request2.content)
                image_carte2 = Image.open(image_data2)
                image_data3 = BytesIO(request3.content)
                image_carte3 = Image.open(image_data3)

                largeur_miniature = 50
                hauteur_miniature = int(largeur_miniature * image_carte1.height / image_carte1.width)
                image_carte1 = image_carte1.resize((largeur_miniature, hauteur_miniature), Image.ANTIALIAS)
                image_carte2 = image_carte2.resize((largeur_miniature, hauteur_miniature), Image.ANTIALIAS)
                image_carte3 = image_carte2.resize((largeur_miniature, hauteur_miniature), Image.ANTIALIAS)
                photo1 = ImageTk.PhotoImage(image_carte1)
                photo2 = ImageTk.PhotoImage(image_carte2)
                photo3 = ImageTk.PhotoImage(image_carte3)

                self.label1 = tk.Label(self.master, image=photo1)
                self.label2 = tk.Label(self.master, image=photo2)
                self.label3 = tk.Label(self.master, image=photo3)
                self.label1.image = photo1
                self.label1.place(x=600, y=400)
                self.label2.image = photo2
                self.label2.place(x=650, y=400)
                self.label3.image = photo3
                self.label3.place(x=700, y=400)

            if len(self.partie.carte_commune) == 4:
                print("non")
                request4 = requests.get(self.partie.carte_commune[3]["image"])

                image_data4 = BytesIO(request4.content)
                image_carte4 = Image.open(image_data4)

                largeur_miniature = 50
                hauteur_miniature = int(largeur_miniature * image_carte4.height / image_carte4.width)
                image_carte4 = image_carte4.resize((largeur_miniature, hauteur_miniature), Image.ANTIALIAS)
                photo4 = ImageTk.PhotoImage(image_carte4)

                self.label4 = tk.Label(self.master, image=photo4)
                self.label4.image = photo4
                self.label4.place(x=750, y=400)

            if len(self.partie.carte_commune) == 5:
                request5 = requests.get(self.partie.carte_commune[4]["image"])

                image_data5 = BytesIO(request5.content)
                image_carte5 = Image.open(image_data5)

                largeur_miniature = 50
                hauteur_miniature = int(largeur_miniature * image_carte5.height / image_carte5.width)
                image_carte5 = image_carte5.resize((largeur_miniature, hauteur_miniature), Image.ANTIALIAS)
                photo5 = ImageTk.PhotoImage(image_carte5)

                self.label5 = tk.Label(self.master, image=photo5)
                self.label5.image = photo5
                self.label5.place(x=800, y=400)
                self.manche_trois()

            self.manche_deux()

        else:
            for joueur in self.partie.list_joueur:
                if joueur.joue_encore is True:
                    self.label.destroy()
                    self.label = tk.Label(self.master, text=f"{joueur} remporte la manche")
                    self.label.place(x=700, y=200)
            Partie.gain_pot(self.partie.en_lice())
            self.partie.next_blind()
            for joueur in self.partie.list_joueur:
                if joueur.pot != 0:
                    joueur.joue_encore = True
                else:
                    joueur.joue_encore = False
            self.manche_un()


    def manche_un(self):
        """
        Gère la première partie de la manche. De la distribution des cartes au flop.
        """
        Partie = Partie_services(self.partie)
        Poker = Poker_DAO()
        for i, joueur in enumerate(self.partie.list_joueur):
            self.label_joueur.append(tk.Label(self.master, text=f"{joueur.name} \n ({joueur.pot} jetons)"))
            self.label_joueur[i].place(x= 40 , y=120*(i+1)-40)
            joueur.main = Poker.draw(self.partie.deck_id, 2)
        self.partie.carte_commune = []
        Partie.ajout_pot(10, self.partie.blind.name)
        for i, joueur in enumerate(self.partie.list_joueur):
            if joueur.name == self.partie.blind.name:
                self.label_joueur[i].destroy()
                self.label_joueur[i] = tk.Label(self.master, text=f"{joueur.name} \n ({joueur.pot} jetons)")
                self.label_joueur[i].place(x= 40 , y=120*(i+1)-40)
        self.partie.next_parle()
        Partie.ajout_pot(20, self.partie.parle.name)
        for i, joueur in enumerate(self.partie.list_joueur):
            if joueur.name == self.partie.parle.name:
                self.label_joueur[i].destroy()
                self.label_joueur[i] = tk.Label(self.master, text=f"{joueur.name} \n ({joueur.pot} jetons)")
                self.label_joueur[i].place(x= 40 , y=120*(i+1)-40)
        self.label.destroy()
        self.label = tk.Label(self.master, text=f"{self.partie.blind.name} a misé 10 et {self.partie.parle.name} a misé 20")
        self.label.place(x=700, y=200)
        self.partie.next_parle()

    def manche_deux(self):
        """
        Gère la deuxième partie de la manche. Du flop au turn et du turn à la river.
        """
        self.partie.mise_max = 0
        self.partie.parle = self.partie.blind
        for i, joueur in enumerate(self.partie.list_joueur):
            self.label_joueur.append(tk.Label(self.master, text=f"{joueur.name} \n ({joueur.pot} jetons)"))
            self.label_joueur[i].place(x= 40 , y=120*(i+1)-40)
            if joueur.pot != 0:
                joueur.joue_encore = True
                joueur.premier_tour = True
        while self.partie.parle.joue_encore is False:
            self.partie.next_parle()
        self.label.destroy()
        self.label = tk.Label(self.master, text=f"{self.partie.parle.name} joue sur {self.partie.mise_max} jetons")
        self.label.place(x=700, y=200)

    def manche_trois(self):
        """
        Gère la troisième manche de la partie. De la river à la fin de manche.
        """
        self.partie.mise_max = 0
        self.partie.parle = self.partie.blind
        for i, joueur in enumerate(self.partie.list_joueur):
            self.label_joueur.append(tk.Label(self.master, text=f"{joueur.name} \n ({joueur.pot} jetons)"))
            self.label_joueur[i].place(x= 40 , y=120*(i+1)-40)
            if joueur.pot != 0:
                joueur.joue_encore = True
                joueur.premier_tour = True
        while self.partie.parle.joue_encore is False:
            self.partie.next_parle()
        self.label.destroy()
        self.label = tk.Label(self.master, text=f"{self.partie.parle.name} joue sur {self.partie.mise_max} jetons")
        self.label.place(x=700, y=200)
