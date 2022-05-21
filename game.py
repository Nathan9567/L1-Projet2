import fltk as fl

from event import Event
import copy
from types import FunctionType

from settings import Settings


class Game:
    """Classe rassemblant les différents éléments pour jouer au jeu."""
    def __init__(self, entities: list, plateau: list, nb_of_grass: int,
                 main_events: FunctionType, save_fun: FunctionType,
                 events: Event, settings: Settings):
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
        self.entities = entities
        self.events = events
        self.sprites = {'B': './media/bush.png', 'G': './media/grass.png'}
        self.plateau = plateau
        self.main_events = main_events
        self.save_fun = save_fun
        self.settings = settings
        self.play(plateau, nb_of_grass)

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
            

    def play(self, plateau, nb_of_grass):
        """Fonction permettant de jouer au jeu.

        Args:
            plateau (list): Plateau de jeu
            nb_of_grass (int): Nombre de touffe d'herbe dans le plateau

        Return None
        """
        if plateau == []:
            return None
        playing = True
        self.states = [copy.deepcopy(self.entities)]
        #print(self.solve(plateau, nb_of_grass))
        print(self.solve_min(plateau, nb_of_grass))
        while playing:
            # temp_map = copy.deepcopy(plateau)
            # for entity in self.entities:
            #     temp_map[entity.x][entity.y] = 'S'
            total_of_grass_occupied = 0
            self.events.get_ev()
            if self.main_events():
                return None
            if self.events.type == "Touche":
                if self.events.data == self.settings['Save']:
                    self.save(plateau)
                elif self.events.data == self.settings['Previous move']:
                    if len(self.states) > 1:
                        self.states.pop()
                        self.entities = copy.deepcopy(self.states[-1])
                elif self.events.data == self.settings['Back']:
                    playing = False
                    return None
                entities_dict = {}
                for entity in self.entities:
                    entity.update(self.events, plateau, entities_dict)
                
                self.replace_entities(entities_dict, self.events.data)
                if self.states[-1] != self.entities:
                    if self.events.data != self.settings['Previous move']:
                        self.states.append(copy.deepcopy(self.entities))
            self.render(plateau)
            if self.isWin(plateau, self.entities, nb_of_grass):
                playing = False
                textsize = int(24 * max(fl.get_width(), fl.get_height()) / 800)
                textx, texty = fl.taille_texte("You win !", taille=textsize)
                fl.texte(fl.get_width()/2 - textx/2,
                         fl.get_height()/2 - texty/2, "You win !",
                         taille=textsize)

            fl.mise_a_jour()
        fl.attente(3)
        fl.efface_tout()

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
            for direction in ["Left", "Right", "Up", "Down"]:
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
                    for direction in ["Left", "Right", "Up", "Down"]:
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
                    fl.image(w/y*py, h/x*px, w/y * (py + 1), h/x*(px + 1),
                             self.sprites[plateau[px][py]], ancrage='sw')

        for entity in self.entities:
            entity.sprite = "./media/sheep.png"
            if plateau[entity.x][entity.y] == 'G':
                entity.sprite = "./media/sheep_grass.png"
            fl.image(w/y*entity.y, h/x*entity.x, w/y * (entity.y + 1),
                     h/x*(entity.x + 1), entity.sprite, ancrage='sw')
