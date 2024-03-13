import tkinter as tk
from tkinter import messagebox

class StartView:
    def __init__(self, master):
        self.master = master
        master.title("Menu principal")

        self.label = tk.Label(master, text="Menu principal")
        self.label.pack()

        self.btn_nouvelle_partie = tk.Button(master, text="Nouvelle Partie", command=self.nouvelle_partie)
        self.btn_nouvelle_partie.pack()

        self.btn_ancienne_partie = tk.Button(master, text="Ancienne Partie", command=self.ancienne_partie)
        self.btn_ancienne_partie.pack()

    def nouvelle_partie(self):
        nouvelle_partie_window = tk.Toplevel(self.master)
        nouvelle_partie_window.title("Nouvelle Partie")

        label_nb_joueurs = tk.Label(nouvelle_partie_window, text="Nombre de joueurs :")
        label_nb_joueurs.pack()

        entry_nb_joueurs = tk.Entry(nouvelle_partie_window)
        entry_nb_joueurs.pack()

        label_nb_jetons = tk.Label(nouvelle_partie_window, text="Nombre de jetons par joueur :")
        label_nb_jetons.pack()

        entry_nb_jetons = tk.Entry(nouvelle_partie_window)
        entry_nb_jetons.pack()

        btn_demarrer_partie = tk.Button(nouvelle_partie_window, text="Démarrer Partie", command=lambda: self.demarrer_partie(entry_nb_joueurs.get(), entry_nb_jetons.get()))
        btn_demarrer_partie.pack()

    def demarrer_partie(self, nb_joueurs, nb_jetons):
        try:
            nb_joueurs = int(nb_joueurs)
            nb_jetons = int(nb_jetons)
            # Vous pouvez implémenter la logique pour démarrer une nouvelle partie avec le nombre de joueurs et de jetons spécifiés ici
            messagebox.showinfo("Nouvelle Partie", f"Nouvelle partie avec {nb_joueurs} joueurs et {nb_jetons} jetons.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides pour le nombre de joueurs et de jetons.")

    def ancienne_partie(self):
        # Implémentez la logique pour charger une ancienne partie ici
        messagebox.showinfo("Ancienne Partie", "Fonctionnalité non encore implémentée.")

def main():
    root = tk.Tk()
    app = StartView(root)
    root.mainloop()

if __name__ == "__main__":
    main()