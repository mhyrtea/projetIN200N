######################
#Groupe 5 TDBI2
#BAISS Salma 
#RODRIGUEZ Diana
#SALIC Awena
#https://github.com/uvsq22101985/projetIN200N
######################
from tkinter import *
import tkinter as tk

#création de l'objet
racine = tk.Tk()
racine.title("Puissance 4")

 #définition de la taille
hauteur = 500
largeur = 500

#taille minimum et maximum
racine.minsize(700, 700)
racine.maxsize(1000, 1000)

racine.iconbitmap(r'C:\Users\novan\Pictures\cat.ico')

#widgets labels 
jouer = tk.Label(racine, bg= "peach puff")
jouer.grid(column= 3, row= 1, padx=5)
label1 = tk.Label(racine, text="Bienvenue:", font =("sitka","20"), bg= "sandy brown")
label2 = tk.Label(racine, text="sur Puissance 4!",font = "sitka", bg = "bisque")
label1.grid(column=3, row=11, padx = 5)
label2.grid(column=3, row=12)


canvas = tk.Canvas(racine, bg="ivory", height=600, width=600)
canvas.grid(column=3, row=2, padx = 100)

#bouton commencer / sart



racine.mainloop()

