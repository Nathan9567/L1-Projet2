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
        self.height = 600
        self.width = 800

    def run(self):
        self.running = True

        # Ouvrir fentre
        fl.cree_fenetre(self.width, self.height,
                        "Ricosheep", "media/sheep.ico")

        print(fl.get_width())
        print(fl.get_height())
        # Bouttons/ Menu
        buttons = list()

        def play():
            self.play()
        buttons.append(Button(200, 250, 600, 350, "Play", play))

        while self.running:
            print(fl.get_width())
            print(fl.get_height())
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
            for i, line in enumerate(f):
                temp = []
                for j, char in enumerate(line):
                    if char == '_':
                        temp.append(None)
                    elif char == 'S':
                        self.entities.append(Sheep(i, j))
                        temp.append(None)
                    elif char == '\n':
                        continue
                    else:
                        temp.append(char)
                plateau.append(temp)
        print(plateau)
        while self.running:
            self.events.get_ev()
            if self.events.type == "Quitte":
                self.running = False
                break
            for entity in self.entities:
                entity.update(self.events, plateau)
            fl.mise_a_jour()

    def render(self, plateau):
        x = len(plateau)
        y = len(plateau[0])
        w = fl.get_width()
        h = fl.get_height()
        for i in range(x):
            pass


app = Application()
app.run()
