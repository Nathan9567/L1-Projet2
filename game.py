import random
import fltk as fl
import copy

from event import Event
from button import Button
from types import FunctionType
from settings import Settings
from sheep import Sheep


class Game:
    """Classe rassemblant les différents éléments pour jouer au jeu."""
    def __init__(self, load_map: FunctionType, main_events: FunctionType,
                 save_fun: FunctionType, events: Event, settings: Settings,
                 menu: FunctionType, screensize: FunctionType):
        """Initialisation du jeu.

        Args:
            entities (list): Liste des entités du jeu
            plateau (list): Plateau de jeu
            nb_of_grass (int): Nombre de touffe d'herbe dans le plateau
            main_events (FunctionType): Fonction permettant de toujours avoir
                                        en execution certains evenements
            save_fun (FunctionType): Fonction permettant de sauvegarder le jeu
            events (Event): Evenements du jeu
        """
        self.entities = list()
        self.events = events
        self.sprites = {'B': './media/bush.png', 'G': './media/grass.png'}
        self.plateau = list()
        self.states = list()
        self.main_events = main_events
        self.save_fun = save_fun
        self.settings = settings
        self.directions = [self.settings["Left"], self.settings["Right"],
                           self.settings["Up"], self.settings["Down"]]
        self.playing = False
        self.menu = menu
        self.load_map = load_map
        self.nb_of_grass = 0
        self.is_screensize_changed = screensize
        self.player()

    def save(self, plateau):
        self.save_fun(plateau, self.entities)

    def replace_entities(self, entities, last_event_data):
        """Fonction permettant de remplacer les entités du jeu.

        Args:
            entities (list): Liste des entités du jeu

        Return None
        """
        if last_event_data == self.settings['Up']:
            for table in entities.values():
                for i, entity in enumerate(table):
                    entity.x += i
        elif last_event_data == self.settings['Down']:
            for table in entities.values():
                for i, entity in enumerate(table):
                    entity.x -= i
        elif last_event_data == self.settings['Left']:
            for table in entities.values():
                for i, entity in enumerate(table):
                    entity.y += i
        elif last_event_data == self.settings['Right']:
            for table in entities.values():
                for i, entity in enumerate(table):
                    entity.y -= i
            

    def graphical_solver(self, plateau, nb_of_grass):
        """Fonction permettant de résoudre le jeu graphiquement.

        Args:
            plateau (list): Plateau de jeu
            nb_of_grass (int): Nombre de touffe d'herbe dans le plateau

        Return:
            list: Liste des mouvements à effectuer pour résoudre le jeu ou None
        """
        solution = self.solve_min(plateau, nb_of_grass)
        print(solution)
        if solution == None:
            fl.texte(fl.get_width()/2, fl.get_height()/2, "No solution found",
                     ancrage='center')
            fl.mise_a_jour()
            fl.attente(1)
            return None
        temp_entities = copy.deepcopy(self.entities)
        for i, move in enumerate(solution):
            entities_dict = {}
            for entity in self.entities:
                entity.update(Event('Touche', move), plateau, entities_dict)
            self.replace_entities(entities_dict, move)
            self.render(plateau)
            fl.mise_a_jour()
            fl.attente(0.5)
            if i == len(solution) - 1:
                fl.texte(fl.get_width()/2, fl.get_height()/2,
                         "It's your turn now !", ancrage='center')
                fl.mise_a_jour()
                fl.attente(0.5)
            fl.efface_tout()
        self.entities = temp_entities
        return solution
    
    def get_key(self, dict, val):
        """Fonction permettant de récupérer la clé d'une valeur dans un dict.

        Args:
            dict (dict): Dictionnaire
            val (any): Valeur de référence

        Returns:
            _type_: _description_
        """
        for key, value in dict.items():
            if val == value:
                return key
    
    def clue(self, plateau, nb_of_grass):
        """Fonction permettant de donner un indice au joueur.

        Args:
            plateau (list): Plateau de jeu
            nb_of_grass (int): Nombre de touffe d'herbe dans le plateau

        Return None
        """
        solution = self.solve_min(plateau, nb_of_grass)
        if solution is None:
            fl.texte(fl.get_width()/2, fl.get_height()/2, "No solution found",
                     ancrage='center')
            fl.mise_a_jour()
            fl.attente(1)
            return None
        fl.texte(fl.get_width()/2, fl.get_height()/2, 'Go ' +
                 self.get_key(self.settings, solution[0]),
                 ancrage='center')
        fl.attente(1)

    def solve(self, plateau, nb_of_grass):
        """Fonction permettant de résoudre le jeu avec un
        algorithme de parcours en profondeur.

        Args:
            plateau (list): Plateau de jeu
            nb_of_grass (int): Nombre de touffe d'herbe dans le plateau

        Returns:
            None: Si le jeu n'est pas résolvable
            list: Liste des mouvements à effectuer pour résoudre le jeu
        """
        states = []

        def __solve(entities):
            state = copy.deepcopy(plateau)
            # for entity in entities:
            #     state[entity.x][entity.y] = 'S'
            if self.isWin(plateau, entities, nb_of_grass):
                return []
            if state in states:
                return None
            states.append(state)
            for direction in self.directions:
                temp_ev = Event("Touche", direction)
                entitiesB = copy.deepcopy(entities)
                temp_entity_dict = {}
                for entity in entitiesB:
                    entity.update(temp_ev, state, temp_entity_dict)
                self.replace_entities(temp_entity_dict, direction)
                result = __solve(entitiesB)
                if result is not None:
                    return [direction] + result
            return None

        return __solve(self.entities)

    def solve_min(self, plateau, nb_of_grass):
        """Fonction permettant de résoudre le jeu avec un
        algorithme de parcours en largeur.

        Args:
            plateau (list): Plateau de jeu
            nb_of_grass (int): Nombre de touffe d'herbe dans le plateau

        Returns:
            None: Si le jeu n'est pas résolvable
            list: Liste des mouvements à effectuer pour résoudre le jeu
        """
        states = []
        state = copy.deepcopy(plateau)
        for entity in self.entities:
            state[entity.x][entity.y] = 'S'
        to_visit = [(state, copy.deepcopy(self.entities), [])]

        def __solve():
            while len(to_visit) != 0:
                state, entities, solution = to_visit.pop(0)
                if self.isWin(plateau, entities, nb_of_grass):
                    return solution
                if state in states:
                    continue
                else:
                    states.append(state)
                    for direction in self.directions:
                        temp_ev = Event("Touche", direction)
                        entitiesB = copy.deepcopy(entities)
                        temp_entity_dict = {}
                        for entity in entitiesB:
                            entity.update(temp_ev, plateau, temp_entity_dict)
                        self.replace_entities(temp_entity_dict, direction)
                        state = copy.deepcopy(plateau)
                        for entity in entitiesB:
                            state[entity.x][entity.y] = 'S'
                        to_visit.append(
                            (state, entitiesB, solution + [direction]))
            return None
        return __solve()

    def isWin(self, plateau, entities, nb_of_grass):
        """Fonction permettant de savoir si le jeu est gagné.

        Args:
            plateau (list): Plateau de jeu
            entities (list): Liste des entités du jeu
            nb_of_grass (int): Nombre de touffe d'herbe dans le plateau

        Returns:
            bool: True si le jeu est gagné, False sinon
        """
        grass_occupied = 0
        for entity in entities:
            if plateau[entity.x][entity.y] == 'G':
                grass_occupied += 1
        if grass_occupied >= nb_of_grass:
            return True
        return False

    def render(self, plateau):
        """Fonction permettant de dessiner le plateau de jeu.

        Args:
            plateau (list): Plateau de jeu

        Return None
        """
        fl.efface_tout()
        fl.rectangle(0, 0, fl.get_width(),
                     fl.get_height(), remplissage='#e0e0e0')
        fl.image(0, 0, fl.get_width(), fl.get_height(), 'media/background.png',
                 ancrage='sw')
        x, y = len(plateau), len(plateau[0])
        w, h = fl.get_width(), fl.get_height()
        for i in range(x):
            fl.ligne(0, h/x*i, w, h/x*i)
        for i in range(y):
            fl.ligne(w/y*i, 0, w/y*i, h)

        for px in range(len(plateau)):
            for py in range(len(plateau[0])):
                if plateau[px][py] is not None:
                    fl.image(w/y*py, h/x*px, w/y * (py + 1), h/x*(px + 1),
                             self.sprites[plateau[px][py]], ancrage='sw')

        for entity in self.entities:
            entity.sprite = "./media/sheep.png"
            if plateau[entity.x][entity.y] == 'G':
                entity.sprite = "./media/sheep_grass.png"
            fl.image(w/y*entity.y, h/x*entity.x, w/y * (entity.y + 1),
                     h/x*(entity.x + 1), entity.sprite, ancrage='sw')

    def player(self):
        """Fonction permettant de jouer au jeu.

        Args:
            plateau (list): Plateau de jeu
            nb_of_grass (int): Nombre de touffe d'herbe dans le plateau

        Return None
        """
        fl.efface_tout()
        self.playing = True
        player_buttons = list()

        def back():
            self.playing = False

        def random_map():
            sol = None
            while sol is None:
                x, y = random.randint(3, 10), random.randint(3, 10)
                sheep = random.randint(1, max(x//2, y//2))
                grass = random.randint(1, sheep)
                temp_grass = grass
                bush = random.randint(4, int(x*y/2))
                temp_plateau = [None for _ in range(y*x)]
                for i in range(len(temp_plateau)):
                    if sheep > 0:
                        temp_plateau[i] = 'S'
                        sheep -= 1
                    elif temp_grass > 0:
                        temp_plateau[i] = 'G'
                        temp_grass -= 1
                    elif bush > 0:
                        temp_plateau[i] = 'B'
                        bush -= 1
                    else:
                        break
                random.shuffle(temp_plateau)
                self.plateau = []
                self.entities = []
                for i in range(y):
                    temp = []
                    for j in range(x):
                        if temp_plateau[i*x + j] == "S":
                            temp.append(None)
                            self.entities.append(Sheep(i, j, self.settings))
                        else:
                            temp.append(temp_plateau[i*x+j])
                    self.plateau.append(temp)
                sol = self.solve_min(self.plateau, grass)
                self.nb_of_grass = grass
            self.play()
        
        def generate_map():
            return
            # TODO
            dim = fl.get_user_input("Dimension de la grille", "longeur:largeur")
            sheep = fl.get_user_input("Nombre de moutons", "int")
            grass = fl.get_user_input("Nombre de touffes d'herbe", "int")
            sol_min = fl.get_user_input("Longueur de la solution minimal", "int")



        def load():
            self.plateau, self.nb_of_grass, self.entities = self.load_map()
            if self.plateau == []:
                return None
            self.playing = False
            self.play()

        player_buttons.append(Button(2, 2, 15, 10, "Back", back))
        player_buttons.append(Button(30, 10, 40, 15, "Load map", load))
        player_buttons.append(Button(30, 45, 40, 15, "Set value", generate_map))
        player_buttons.append(Button(30, 65, 40, 15, "Just random", random_map))

        fl.texte(35/100*fl.get_width(), 35/100*fl.get_height(), 'Random map :',
                 taille=int(10/100 * fl.get_height() * 0.5),
                 police='Helvetica', couleur='black', ancrage='nw')
        while self.playing:
            if self.menu(player_buttons):
                return None
            if self.events.type == "Touche":
                if self.events.data == self.settings['Back']:
                    self.playing = False
            fl.mise_a_jour()

    def play(self):
        if self.plateau == []:
            self.playing = False
            return None
        self.render(self.plateau)
        playing = True
        self.states = [copy.deepcopy(self.entities)]
        # print(self.solve(plateau, nb_of_grass))
        # print(self.solve_min(self.plateau, self.nb_of_grass))
        while playing:
            # temp_map = copy.deepcopy(plateau)
            # for entity in self.entities:
            #     temp_map[entity.x][entity.y] = 'S'
            self.events.get_ev()
            if self.main_events():
                return None
            if self.is_screensize_changed():
                self.render(self.plateau)
            if self.events.type == "Touche":
                if self.events.data == self.settings['Save']:
                    self.save(self.plateau)
                elif self.events.data == self.settings['Previous move']:
                    if len(self.states) > 1:
                        self.states.pop()
                        self.entities = copy.deepcopy(self.states[-1])
                elif self.events.data == self.settings['Back']:
                    playing = False
                    self.playing = False
                    return None
                elif self.events.data == self.settings['Solver']:
                    self.graphical_solver(self.plateau, self.nb_of_grass)
                    self.render(self.plateau)
                    continue
                elif self.events.data == self.settings['Clue']:
                    self.clue(self.plateau, self.nb_of_grass)
                    self.render(self.plateau)
                    continue
                entities_dict = {}
                for entity in self.entities:
                    entity.update(self.events, self.plateau, entities_dict)
                
                self.replace_entities(entities_dict, self.events.data)
                if self.states[-1] != self.entities:
                    if self.events.data != self.settings['Previous move']:
                        self.states.append(copy.deepcopy(self.entities))
                self.render(self.plateau)
            if self.isWin(self.plateau, self.entities, self.nb_of_grass):
                playing = False
                textsize = int(24 * max(fl.get_width(), fl.get_height()) / 800)
                textx, texty = fl.taille_texte("You win !", taille=textsize)
                fl.texte(fl.get_width()/2 - textx/2,
                        fl.get_height()/2 - texty/2, "You win !",
                        taille=textsize)

            fl.mise_a_jour()
        fl.attente(3)
        fl.efface_tout()

