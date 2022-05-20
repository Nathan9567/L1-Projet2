import fltk as fl

from event import Event
from button import Button
from tkinter import filedialog
import copy
from sheep import *
from types import FunctionType

class Game():

    def __init__(self, entities: list, plateau: list, nb_of_grass: int, main_events: FunctionType, save_fun: FunctionType, events: Event):
        self.entities = entities
        self.events = events
        self.sprites = {'B': './media/bush.png', 'G': './media/grass.png'}
        self.plateau = plateau
        self.main_events = main_events
        self.save_fun = save_fun
        self.play(plateau, nb_of_grass)

    def save(self, plateau):
        self.save_fun(plateau, self.entities)


    def play(self, plateau, nb_of_grass):
        if plateau == []:
            return None
        playing = True
        self.states = [copy.deepcopy(self.entities)]
        # print(self.solve(plateau, nb_of_grass))
        # print(self.solve_min(plateau, nb_of_grass))
        while playing:
            # temp_map = copy.deepcopy(plateau)
            # for entity in self.entities:
            #     temp_map[entity.x][entity.y] = 'S'
            total_of_grass_occupied = 0
            self.events.get_ev()
            if self.main_events(): 
                return None
            if self.events.type == "Touche":
                if self.events.data == "F2":
                    self.save(plateau)
                elif self.events.data == "F3":
                    if len(self.states) > 1:
                        self.states.pop()
                        self.entities = copy.deepcopy(self.states[-1])
                entities_dict = {}
                for entity in self.entities:
                    entity.update(self.events, plateau)
                    if entity.sprite == "./media/sheep_grass.png":
                        total_of_grass_occupied += 1
                if self.states[-1] != self.entities and self.events.data != "F3":
                    self.states.append(copy.deepcopy(self.entities))
                print(plateau)
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
        print(plateau)
        fl.efface_tout()
        fl.rectangle(0, 0, fl.get_width(),
                     fl.get_height(), remplissage='#e0e0e0')
        # fl.image(0, 0, fl.get_width(), fl.get_height(),
        #          './media/background.png', ancrage='sw')
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
