import fltk as fl

from event import Event
from button import Button 
from tkinter import filedialog
from sheep import *


class Application:

    def __init__(self):
        self.entities = list()
        self.running = False
        self.events = Event("", None)

    
    def run(self):
        self.running = True
        
        # Ouvrir fentre
        fl.cree_fenetre(800, 600)

        # Bouttons/ Menu
        buttons = list()
        def play():
            self.play()
        buttons.append(Button(200, 250, 600, 350, "Play", play))

        while self.running:
            self.events.get_ev()
            if self.events.type == "Quitte":
                self.running = False
                break
            
            for button in buttons:
                button.update(self.events)
            fl.mise_a_jour()
        fl.ferme_fenetre()
        

    def play(self):
        # ouvrir file dialog
        # peupler not table 'entities' avec le fichier
        file_path = filedialog.askopenfilename()
        plateau = list()
        with open(file_path, 'r') as f:
            for line, i in enumerate(f):
                temp = []
                for char, j in enumerate(line):
                    if char == '_':
                        temp.append(None)
                    elif char == 'S':
                        self.entities.append(Sheep(i,j))
                        temp.append(None)
                    else:
                        temp.append(char)
                plateau.append(temp)


        #while self.running:
        #   on prend les inputs
        #   on affiche le background
        #   for entity in entities:
        #   entity.update()

        
app = Application()
app.run()