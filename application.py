import fltk as fl

from event import Event
from button import Button
from tkinter import filedialog
from settings import Settings
from sheep import Sheep
from game import Game
from editor import Editor


class Application:
    """Classe rassemblant les différents éléments pour programme final."""

    def __init__(self):
        """Constructeur de la classe Application."""
        self.running = False
        self.events = Event("", None)
        self.height = 600
        self.width = 800
        self.fullscreen = False
        self.dict_settings = {'Up': 'Up', 'Down': 'Down', 'Left': 'Left',
                              'Right': 'Right', 'Save': 'F12',
                              'Fullscreen': 'F11', 'Back': 'Escape',
                              'Previous move': 'F3', 'Solver': 'F4',
                              'Clue': 'F1'}
        self.screensize = (self.width, self.height)
        self.background = False

    def run(self):
        """Fonction permettant de lancer le programme.

        Return None
        """
        self.running = True
        self.background = False
        # Ouvrir fentre
        fl.cree_fenetre(self.width, self.height,
                        "Ricosheep", "media/sheep.ico")

        # Bouttons/ Menu
        buttons = list()

        # Fonctions pour les boutons
        def main_events(): return self.main_events()

        def save(plateau, entities):
            self.save(plateau, entities)

        def savetxt(plateau):
            self.savetxt(plateau)

        def menu(buttons):
            return self.menu(buttons)

        def load_map():
            return self.load_map()
        
        def screen_size():
            return self.is_screensize_change()

        def play():
            self.background = False
            Game(load_map, main_events, save, self.events,
                 self.dict_settings, menu, screen_size)

        def editor():
            self.background = False
            self.events = Event("", None)
            Editor(menu, load_map, savetxt, self.events, self.dict_settings, screen_size)

        def how_to_play():
            self.background = False
            self.how_to_play()

        def settings(bool):
            self.background = False
            setting = Settings(menu, self.events, self.dict_settings, screen_size)
            if bool is True:
                setting.settings()
                self.dict_settings = setting.get_settings()
                return None
            return setting

        buttons.append(Button(2, 2, 10, 12, "", settings, True))
        buttons.append(Button(30, 25, 40, 15, "Play", play))
        buttons.append(Button(30, 45, 40, 15, "Editor", editor))
        buttons.append(Button(30, 65, 40, 15, "Rules", how_to_play))
        # buttons.append(Button(200, 250, 600, 350, "Random Map", play))

        settings(False).import_settings()
        self.dict_settings = settings(False).get_settings()

        # Boucle principale
        while self.running:
            fl.efface('b')
            if not self.background or self.is_screensize_change():
                fl.image(0, 0, fl.get_width(), fl.get_height(),
                         './media/background/Ricosheep.png', ancrage='sw')
                self.background = True
            self.menu(buttons)
            fl.image(2/100 * fl.get_width(), 2/100 * fl.get_height(),
                     12/100 * fl.get_width(), 14/100 * fl.get_height(),
                     "media/gear.png", ancrage='sw')
            fl.mise_a_jour()

        settings(False).save_settings()
        fl.ferme_fenetre()

    def how_to_play(self):
        """Fonction permettant d'afficher le menu de l'aide.

        Returns:
            bool: True si l'utilisateur veut quitter le programme, None sinon.
        """
        while True:
            fl.efface_tout()
            self.events.get_ev()
            if self.main_events():
                return True
            explanation = ["The goal is to fill all the grass with a sheep.",
                           "You can move the sheep with the arrow keys.",
                           "If you want to see or edit controls, you can",
                           "back to the menu by pressing a key and click",
                           "on the gear icon at the top left corner."]
            w = fl.get_width()
            h = fl.get_height()
            fl.texte(w/2, 10/100 * h, "How to play :", couleur='black',
                     ancrage='center', police='Helvetica', taille=28)
            for i, text in enumerate(explanation):
                fl.texte(w/2, (22 + (i*6))/100 * h, text, couleur='black',
                         ancrage='center', police='Helvetica', taille=20)
            fl.mise_a_jour()

            if self.events.type is not None:
                return True

    def menu(self, buttons):
        """Fonction permettant d'afficher certains boutons dans la fenetre.

        Return None"""
        fl.efface('b')
        self.events.get_ev()
        for button in buttons:
            button.update(self.events)

        if self.main_events():
            return True

    def main_events(self):
        """Fonction permettant de gérer les évènements nécessaire
        au bon fonctionnement du programme.

        Returns:
            bool: True si l'utilisateur veut quitter le programme, False sinon.
        """
        if self.events.type == "Quitte":
            self.running = False
            return True
        elif self.events.type == "Touche" and self.events.data == "F11":
            self.fullscreen = not self.fullscreen
            fl.set_fullscreen(self.fullscreen)

    def load_map_txt(self, file_path, plateau, entities, number_of_grass):
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                temp = []
                for j, char in enumerate(line):
                    if char == '_':
                        temp.append(None)
                    elif char == 'S':
                        entities.append(Sheep(i, j, self.dict_settings))
                        temp.append(None)
                    elif char == 'G':
                        number_of_grass += 1
                        temp.append(char)
                    elif char == '\n':
                        continue
                    else:
                        temp.append(char)
                plateau.append(temp)
        return plateau, entities, number_of_grass

    def load_map_save(self, file_path, plateau, entities, number_of_grass):
        with open(file_path, 'r') as f:
            for line in f:
                if line[0] == '&':
                    coord = line[1:-1].split(',')
                    entities.append(
                        Sheep(int(coord[0]), int(coord[1]),
                              self.dict_settings))
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
        return plateau, entities, number_of_grass

    def load_map(self):
        """Fonction permettant de charger un fichier de map.

        Returns:
            list: Liste de liste de str représentant le plateau.
            int: Nombre de tuile de grass.
            list: Liste d'entités représentant les Sheep.
        """
        entities = list()
        file_path = filedialog.askopenfilename(
            filetypes=[("Map File", "*.txt"), ("Save File", "*.sav"),
                       ("All", "*")], defaultextension='.txt')
        if file_path == '':
            return [], 0, []
        plateau = list()
        number_of_grass = 0
        extension = file_path.split('.')[-1]
        if extension == 'txt':
            plateau, entities, number_of_grass = self.load_map_txt(
                file_path, plateau, entities, number_of_grass)
        elif extension == 'sav':
            plateau, entities, number_of_grass = self.load_map_save(
                file_path, plateau, entities, number_of_grass)
        else:
            return [], 0, []
        return plateau, number_of_grass, entities

    def save(self, plateau, entities):
        """Fonction afin de sauvegarder le plateau dans un fichier de
        sauvegarde (.sav).

        Args:
            plateau (list): Liste de liste de str représentant le plateau.
            entities (list): Liste d'entités représentant les Sheep.

        Return None
        """
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
            for sheep in entities:
                f.write('&' + str(sheep.x) + ',' + str(sheep.y) + '\n')

    def savetxt(self, plateau):
        """Fonction permettant de sauvegarder le plateau dans un fichier
        de map (.txt).

        Args:
            plateau (list): Liste de liste de str représentant le plateau.

        Return None
        """
        file_path = filedialog.asksaveasfilename(
            filetypes=[("Text File", "*.txt"), ("All", "*")],
            defaultextension='.txt')
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

    def is_screensize_change(self):
        if self.screensize != (fl.get_width(), fl.get_height()):
            self.screensize = (fl.get_width(), fl.get_height())
            return True
        return False
