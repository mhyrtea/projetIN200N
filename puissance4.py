######################
#Groupe 5 TDBI2
#BAISS Salma 
#RODRIGUEZ Diana
#SALIC Awena
#https://github.com/uvsq22101985/projetIN200N
######################
# Variables
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import random

from pkg_resources import get_default_cache

WIDTH = 560
HEIGHT = 560
largeur_case = WIDTH // 7
hauteur_case = HEIGHT // 6
color = "#18534F"
player_1 = 1
player_2 = 2 
player_turn = ""
grille = [[0] * 7 for i in range(6)]                # le tableau fait 7 colonnes de 6 lignes
gagne = False
lst = []


#############################
# Fonctions
def get_button(b):
    global gagne
    global lst

    if gagne: return
    joueur = player_turn
    x = b-1
    y = playable_grid(player_colour, x, grille)
    # pas la peine de tester les alignements si il y a moins de 7 jetons dans la grille
    changement_joueur()
    if len(lst) < 7: return

    gagne = test_alignement (x, y)
    if gagne:
        mb.showinfo (title="Partie terminée", message="Le vainqueur est " + joueur)
    if len(lst) == 42:              # Grille pleine
        mb.showinfo (title="Partie terminée", message="Match nul !!")


def test_alignement(x, y):
    
    nb_jetons = 0
    # test alignement vertical
    if (y < 3):                 # pas la peine de tester en vertical si il y a moins de 4 jetons dans la colonne
        for i in range (5):
           if grille [i][x] == grille [i+1][x] and grille [i][x] != 0:
                nb_jetons += 1
                if nb_jetons == 3:             # 3 parce que 3 comparaisons suffisent
                    return True
           else:
             nb_jetons = 0
 
    nb_jetons = 0
    # test alignement horizontal
    for i in range (6):
         if grille [y][i] == grille [y][i+1] and grille [y][i] != 0:
            nb_jetons += 1
            if nb_jetons == 3:              # 3 parce que 3 comparaisons suffisent
                return True
         else:
            nb_jetons = 0

    # Pour les tests d'alignement, on va considérer qu'on travaille sur une matrice de 7 * 7 car c'est dans elle qu'on peut trouver un alignement
    # En fait, le cercle dessiné se trouve au centre de celle-ci

    nb_jetons = 0
    # test alignement diagonal ascendant de gauche à droite
    j = y + 3
    for i in range(x-3,x+3):
        if i >= 0 and i < 6:
            if j > 0 and j < 6:
                if grille [j][i] == grille [j-1][i+1] and grille [j][i] != 0 and grille [j-1][i+1] != 0:
                    nb_jetons += 1
                    if nb_jetons == 3:              # 3 parce que 3 comparaisons suffisent
                        return True
                else:
                    nb_jetons = 0
            j -= 1

    nb_jetons = 0
    # test alignement diagonal ascendant de droite à gauche
    j = y + 3;
    for i in range(x+3,x-3, -1):
        if i >= 0 and i < 6:
           if j >= 0 and j < 6:
              if grille [j][i] == grille [j-1][i-1] and grille [j][i] != 0 and grille [j-1][i-1] != 0:
                  nb_jetons += 1
                  if nb_jetons == 3:              # 3 parce que 3 comparaisons suffisent
                     return True
              else:
                  nb_jetons = 0
           j -= 1
        
 
def set_grid(grille):
    # Fonction qui remets la grille à 0
    for i in range(7):
        for j in range(6):
            grille[j][i] = 0
    return(grille)

def annuler_coup():
    # Fonction qui permet de revenir un coup en arrière
    # le dernier coup est le dernier élément de la liste lst
    # On prend le numéro de l'objet, on supprime celui-ci du canvas et on le vire de la liste lst
    global gagne
    lst_lue = []
    taille = len (lst)
    if taille == 0: return
    ligne = lst[len(lst) - 1]
    lst_lue = ligne.split(",")
    x = int(lst_lue[1])
    y = int(lst_lue[2])
    grille[y][x] = 0
    obj = int (lst_lue[3])              # 3 c'est la position de la référence de l'objet dans la ligne de la liste
    canvas.delete (obj)
    lst.remove(ligne)
    changement_joueur()         # Permet au joueur qui a annulé son coup de rejouer
    gagne = False               # Permet également si la partie est terminée de rejouer
    return


def load():
    # Fonction qui permet de charger une partie déjà sauvegardée
    global gagne
    global lst
    x = 0
    y = 0
    filetypes = (('Fichier texte', '*.txt'), ('Tous les fichiers', '*.*'))
    lst_lue = []
    # Affiche la fenêtre pour sélectionner le fichier
    filename = fd.askopenfile(filetypes=filetypes)
    if filename is None: return               # Pas de fichier choisi
    f = open (filename.name, "r")
    first_line = True
    last_line = False
    for line in f:
        if first_line:
            # Si le fichier ne commence pas par Fichier Puissance 4, ce n'est pas une sauvegarde. Fait pour éviter de charger n'importe quel fichier
            if line != "Fichier Puissance 4\n": return
            first_line = False
            canvas.delete("all")
            set_grid (grille)
            lst.clear()
            # Création de la grille
            for i in range(7):
                for j in range(6):
                    canvas.create_rectangle((i*largeur_case, j*hauteur_case),
                        ((i+1)*largeur_case, (j+1)*hauteur_case), fill=color)
            continue
        if line == "True":                  # la dernière ligne du fichier permet de savoir si la partie était terminée, ce qui bloque les boutons des colonnes
            gagne = True
            continue
        lst_lue = line.split(",")
        player_colour = lst_lue [0]
        x = int(lst_lue [1])
        y = int (lst_lue [2])
        gauche = largeur_case * x
        droite = gauche + largeur_case
        haut = hauteur_case * y
        bas = haut + hauteur_case
        # mettre dans une variable la référence à l'objet que l'on va créer pour pouvoir le supprimer ensuite pour le undo
        obj = canvas.create_oval(((gauche, haut),(droite, bas)) , fill=player_colour)
        grille[y][x] = player_colour
        lst.append(player_colour + "," + str(x) + "," + str(y) + "," + str(obj) )
        canvas.update()
    f.close()
    return
   

def save():
    # Fonction qui permet de sauvegarder une partie en cours
    global gagne
    global lst

    filetypes = (('Fichier texte', '*.txt'), ('Tous les fichiers', '*.*'))
    # Affiche la fenêtre pour sélectionner le fichier
    filename = fd.asksaveasfilename(filetypes=filetypes)
    if filename == "" or filename is None: return               # Pas de fichier choisi
    f = open (filename, "w")
    f.write("Fichier Puissance 4\n")
    for i in range (len (lst)):
        f.write(lst[i] + "\n")
    f.write(str(gagne))
    f.close()
    return

def new_game():
    # Fonction qui permet de démarrer une nouvelle partie
    # la fonction set_grille au dessus peut aider pour remettre la grille à zéro
    global gagne
    global grille

    canvas.delete("all")
    set_grid (grille)
    lst.clear()
    # Création de la grille
    for i in range(7):
        for j in range(6):
            canvas.create_rectangle((i*largeur_case, j*hauteur_case), ((i+1)*largeur_case, (j+1)*hauteur_case), fill=color)
    gagne = False
    return

def playable_grid(player_colour, x, grille):
    # Fonction qui va lancer le jeu et verifier, ligne par ligne,
    # dans la colonne choisie par le joueur
    # s'il y a ou non des obstacles
    global lst
    y = 5
    
    while(grille[y][x] != 0):
        y -=1
        if (y < 0):
            return y
    if(grille[y][x] == 0):
        gauche = largeur_case * x
        droite = gauche + largeur_case
        haut = hauteur_case * y
        bas = haut + hauteur_case
        # mettre dans une variable la référence à l'objet que l'on va créer pour pouvoir le supprimer ensuite pour le undo
        obj = canvas.create_oval(((gauche, haut),(droite, bas)) , fill=player_colour)
        grille[y][x] = player_colour
        lst.append(player_colour + "," + str(x) + "," + str(y) + "," + str(obj) )
        canvas.update()
    return y

def beginner_player():
    global player_colour, player_turn
    global beginner, choice_colour
    couleurs = ["red", "yellow"]
    choice_colour = random.choice(couleurs)
    if choice_colour == "red":
        player_turn = "Joueur 1"
        player_colour = "red"
    else:
        player_turn = "Joueur 2"
        player_colour = "yellow"
    beginner = tk.Label(racine, text = player_turn, fg = player_colour, bg = "#535953")
    beginner.grid(row=8, column = 3, columnspan=3)
    

def changement_joueur():
    global player_colour, player_turn
    global beginner
    if player_turn == "Joueur 1":
        player_turn = "Joueur 2"
        player_colour = "yellow"
    else:
        player_turn = "Joueur 1"
        player_colour = "red"
    beginner = tk.Label(racine, text = player_turn, fg = player_colour, bg = "#535953")
    beginner.grid(row=8, column = 3, columnspan=3)

#############################
# Programme Principal #

racine = tk.Tk()
racine.title("Puissance 4")

canvas = tk.Canvas(racine, width=WIDTH, height= HEIGHT, bg = '#226D68')

# Création de la grille
for i in range(7):
    for j in range(6):
        canvas.create_rectangle((i*largeur_case, j*hauteur_case), ((i+1)*largeur_case, (j+1)*hauteur_case), fill=color)

# Boutons
bouton_annuler = ttk.Button(racine, text = "Retour", command=lambda:annuler_coup())
bouton_save = ttk.Button(racine, text="Sauvegarder", command=lambda:save())
bouton_load = ttk.Button(racine, text="Charger", command=lambda:load())
bouton_newgame = ttk.Button(racine, text = "Nouvelle partie", command=lambda:new_game())
bouton_column1 = ttk.Button(racine, text = "1", command=lambda:get_button(1))
bouton_column2 = ttk.Button(racine, text = "2", command=lambda:get_button(2))
bouton_column3 = ttk.Button(racine, text = "3", command=lambda:get_button(3))
bouton_column4 = ttk.Button(racine, text = "4", command=lambda:get_button(4))
bouton_column5 = ttk.Button(racine, text = "5", command=lambda:get_button(5))
bouton_column6 = ttk.Button(racine, text = "6", command=lambda:get_button(6))
bouton_column7 = ttk.Button(racine, text = "7", command=lambda:get_button(7))


# Placements des widgets/boutons
bouton_annuler.grid(row = 8, column = 1, columnspan=1)
bouton_save.grid(row =8, column = 7, columnspan= 1)
bouton_load.grid(row = 8, column = 6, columnspan= 1)
bouton_newgame.grid(row = 8, column = 2, columnspan=1)
bouton_column1.grid(row = 0, column = 1)
bouton_column2.grid(row = 0, column = 2)
bouton_column3.grid(row = 0, column = 3)
bouton_column4.grid(row = 0, column = 4)
bouton_column5.grid(row = 0, column = 5)
bouton_column6.grid(row = 0, column = 6)
bouton_column7.grid(row = 0, column = 7)
canvas.grid(row=1, column=1, columnspan=7)

beginner_player()
racine.mainloop()