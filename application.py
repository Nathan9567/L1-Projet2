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
        self.states = list()
        self.main_buttons = list()

    def run(self):
        self.running = True

        # Ouvrir fentre
        fl.cree_fenetre(self.width, self.height,
                        "Ricosheep", "media/sheep.ico")

        # Bouttons/ Menu
        buttons = self.main_buttons

        def play():
            plateau, nb_of_grass = self.load_map()
            self.play(plateau, nb_of_grass)
        
        def editor():
            self.editor()


        # buttons.append(Button(200, 250, 600, 350, "Play", play))
        buttons.append(Button(25, 25, 40, 20, "Play", play))
        buttons.append(Button(25, 50, 40, 20, "Editor", editor))
        # buttons.append(Button(200, 250, 600, 350, "Random Map", play))

        while self.running:
            self.menu(buttons)

        fl.ferme_fenetre()

    
    def menu(self, buttons):
        fl.efface_tout()
        self.events.get_ev()
        if self.main_events(): return True

        for button in buttons:
            button.update(self.events)
        fl.mise_a_jour()


    def main_events(self):
        if self.events.type == "Quitte":
            self.running = False
            return True
        elif self.events.type == "Touche" and self.events.data == "F11":
            self.fullscreen = not self.fullscreen
            fl.set_fullscreen(self.fullscreen)
    
    
    def load_map(self):
        self.entities = list()
        file_path = filedialog.askopenfilename(
            filetypes=[("Map File", "*.txt"), ("Save File", "*.sav"),
                       ("All", "*")], defaultextension='.txt')
        if file_path == '':
            return [], 0
        plateau = list()
        number_of_grass = 0
        extension = file_path.split('.')[-1]
        if extension == 'txt':
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
        elif extension == 'sav':
            with open(file_path, 'r') as f:
                for line in f:
                    if line[0] == '&':
                        coord = line[1:-1].split(',')
                        self.entities.append(
                            Sheep(int(coord[0]), int(coord[1])))
                        continue
                    temp = []
                    for char in line:
                        if char == '_':
                            temp.append(None)
                        elif char == 'G':
                            number_of_grass += 1
                            temp.append(char)
                        elif char == '\n':
                            continue
                        else:
                            temp.append(char)
                    plateau.append(temp)
        else:
            return [], 0
        return plateau, number_of_grass


    def play(self, plateau, nb_of_grass):
        if plateau == []:
            return None
        playing = True
        self.states = [copy.deepcopy(self.entities)]
        # print(self.solve(plateau, nb_of_grass))
        print(self.solve_min(plateau, nb_of_grass))
        while playing:
            total_of_grass_occupied = 0
            self.events.get_ev()
            if self.main_events(): return None
            if self.events.type == "Touche":
                if self.events.data == "F2":
                    self.save(plateau)
                elif self.events.data == "F3":
                    if len(self.states) > 1:
                        self.states.pop()
                        self.entities = copy.deepcopy(self.states[-1])
            temp_map = copy.deepcopy(plateau)
            for entity in self.entities:
                temp_map[entity.x][entity.y] = 'S'
            for entity in self.entities:
                entity.update(self.events, temp_map)
                if entity.sprite == "./media/sheep_grass.png":
                    total_of_grass_occupied += 1
            if self.states[-1] != self.entities and self.events.data != "F3":
                self.states.append(copy.deepcopy(self.entities))
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

        def __solve(entities):
            state = copy.deepcopy(plateau)
            for entity in entities:
                state[entity.x][entity.y] = 'S'
            if self.isWin(plateau, entities, nb_of_grass):
                return []
            if state in states:
                return None
            states.append(state)
            for direction in ["Left", "Right", "Up", "Down"]:
                temp_ev = Event("Touche", direction)
                entitiesB = copy.deepcopy(entities)
                for entity in entitiesB:
                    entity.update(temp_ev, state)
                result = __solve(entitiesB)
                if result is not None:
                    return [direction] + result
            return None

        return __solve(self.entities)


    def solve_min(self, plateau, nb_of_grass):
        states = []
        state = copy.deepcopy(plateau)
        for entity in self.entities:
            state[entity.x][entity.y] = 'S'
        to_visit = [(state, copy.deepcopy(self.entities), [])]

        def __solve():
            while len(to_visit) != 0:
                state, entities, solution = to_visit.pop(0)
                # print(state)
                if self.isWin(plateau, entities, nb_of_grass):
                    return solution
                if state in states:
                    continue
                else:
                    states.append(state)
                    for direction in ["Left", "Right", "Up", "Down"]:
                        temp_ev = Event("Touche", direction)
                        entitiesB = copy.deepcopy(entities)
                        state = copy.deepcopy(plateau)
                        for entity in entities:
                            state[entity.x][entity.y] = 'S'
                        for entity in entitiesB:
                            entity.update(temp_ev, state)
                        state = copy.deepcopy(plateau)
                        for entity in entitiesB:
                            state[entity.x][entity.y] = 'S'
                        to_visit.append(
                            (state, entitiesB, solution + [direction]))
            return None
        return __solve()


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


    def save(self, plateau):
        file_path = filedialog.asksaveasfilename(
            filetypes=[("Save File", "*.sav"), ("All", "*")],
            defaultextension='.sav')
        if file_path == '':
            return
        with open(file_path, 'w') as f:
            for line in plateau:
                for char in line:
                    if char is None:
                        f.write('_')
                    else:
                        f.write(char)
                f.write('\n')
            for sheep in self.entities:
                f.write('&' + str(sheep.x) + ',' + str(sheep.y) + '\n')


    def editor(self):
        fl.efface_tout()
        edit = True
        self.events = Event("", None)
        plateau = []
        edit_buttons = []
        def back():
            self.menu(self.main_buttons)
            return True
        def items(item):
            return item
        edit_buttons.append(Button(0, 0, 10, 10, 'Back', back))
        edit_buttons.append(Button(0, 10, 10, 10, 'Save', self.save, plateau))
        edit_buttons.append(Button(0, 20, 10, 10, 'Sheep', items, 'Sheep'))
        edit_buttons.append(Button(0, 30, 10, 10, 'Grass', items, 'Grass'))
        edit_buttons.append(Button(0, 40, 10, 10, 'Bush', items, 'Bush'))
        while edit:
            if self.menu(edit_buttons):
                edit = False


app = Application()
app.run()
