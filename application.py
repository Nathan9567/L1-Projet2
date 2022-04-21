import fltk as fl

from event import Event
from button import Button
from tkinter import filedialog
import copy
from sheep import *


class Application:

    def __init__(self):
        self.entities = list()
        self.running = False
        self.events = Event("", None)
        self.height = 600
        self.width = 800
        self.fullscreen = False
        self.sprites = {'B': './media/bush.png', 'G': './media/grass.png'}

    def run(self):
        self.running = True

        # Ouvrir fentre
        fl.cree_fenetre(self.width, self.height,
                        "Ricosheep", "media/sheep.ico")

        # Bouttons/ Menu
        buttons = list()

        def play():
            plateau, nb_of_grass = self.load_map()
            self.play(plateau, nb_of_grass)

        buttons.append(Button(200, 250, 600, 350, "Play", play))

        while self.running:
            self.events.get_ev()
            if self.events.type == "Quitte":
                self.running = False
                break
            elif self.events.type == "Touche" and self.events.data == "F11":
                self.fullscreen = not self.fullscreen
                fl.set_fullscreen(self.fullscreen)

            for button in buttons:
                button.update(self.events)
            fl.mise_a_jour()
        fl.ferme_fenetre()

    def load_map(self):
        self.entities = list()
        file_path = filedialog.askopenfilename()
        if file_path == '':
            return [], 0
        plateau = list()
        number_of_grass = 0
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                temp = []
                for j, char in enumerate(line):
                    if char == '_':
                        temp.append(None)
                    elif char == 'S':
                        self.entities.append(Sheep(i, j))
                        temp.append(None)
                    elif char == 'G':
                        number_of_grass += 1
                        temp.append(char)
                    elif char == '\n':
                        continue
                    else:
                        temp.append(char)
                plateau.append(temp)
        return plateau, number_of_grass

    def play(self, plateau, nb_of_grass):
        if plateau == []:
            return None
        playing = True
        print(self.solve(plateau, nb_of_grass))
        while playing:
            total_of_grass_occupied = 0
            self.events.get_ev()
            if self.events.type == "Quitte":
                self.running = False
                return None
            elif self.events.type == "Touche" and self.events.data == "F11":
                self.fullscreen = not self.fullscreen
                fl.set_fullscreen(self.fullscreen)
            temp_map = copy.deepcopy(plateau)
            for entity in self.entities:
                temp_map[entity.x][entity.y] = 'S'
            for entity in self.entities:
                entity.update(self.events, temp_map, self.entities)
                if entity.sprite == "./media/sheep_grass.png":
                    total_of_grass_occupied += 1
            self.render(plateau)
            if self.isWin(plateau, self.entities, nb_of_grass):
                playing = False
                textsize = int(24 * max(fl.get_width(), fl.get_height()) / 800)
                textx, texty = fl.taille_texte("You win !", taille=textsize)
                fl.texte(fl.get_width()/2 - textx/2,
                         fl.get_height()/2 - texty/2, "You win !", taille=textsize)

            fl.mise_a_jour()
        fl.attend_clic_gauche()
        fl.efface_tout()

    def solve(self, plateau, nb_of_grass):

        states = []

        def __solve(entities, solution):
            if solution != []:

                temp_ev = Event("Touche", solution[-1])
                temp_map = copy.deepcopy(plateau)
                entities = copy.deepcopy(entities)
                state = []
                for entity in entities:
                    temp_map[entity.x][entity.y] = 'S'
                # print(states)
                states.append(temp_map)
                for entity in entities:
                    entity.update(temp_ev, temp_map, self.entities)
                    state.append((entity.x, entity.y))

                states.append(state)
                if self.isWin(plateau, entities, nb_of_grass):
                    return solution
                if state not in states:
                    return min([__solve(entities, solution+["Left"]), __solve(entities, solution+["Right"]),
                                __solve(entities, solution+["Up"]), __solve(entities, solution+["Down"])], key=len)

        return __solve(self.entities, [])

    def isWin(self, plateau, entities, nb_of_grass):
        grass_occupied = 0
        for entity in entities:
            if plateau[entity.x][entity.y] == 'G':
                grass_occupied += 1
        if grass_occupied >= nb_of_grass:
            return True
        return False

    def render(self, plateau):
        fl.efface_tout()
        fl.rectangle(0, 0, fl.get_width(),
                     fl.get_height(), remplissage='#e0e0e0')
        x, y = len(plateau), len(plateau[0])
        w, h = fl.get_width(), fl.get_height()
        for i in range(x):
            fl.ligne(0, h/x*i, w, h/x*i)
        for i in range(y):
            fl.ligne(w/y*i, 0, w/y*i, h)

        for px in range(len(plateau)):
            for py in range(len(plateau[0])):
                if plateau[px][py] is not None:
                    fl.image(w/y*py, h/x*px, w/y *
                             (py + 1), h/x*(px + 1), self.sprites[plateau[px][py]], ancrage='sw')

        for entity in self.entities:
            entity.sprite = "./media/sheep.png"
            if plateau[entity.x][entity.y] == 'G':
                entity.sprite = "./media/sheep_grass.png"
            fl.image(w/y*entity.y, h/x*entity.x, w/y *
                     (entity.y + 1), h/x*(entity.x + 1), entity.sprite, ancrage='sw')


app = Application()
app.run()
