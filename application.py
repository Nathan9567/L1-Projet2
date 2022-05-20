import fltk as fl

from event import Event
from button import Button
from tkinter import filedialog
from sheep import Sheep
from game import Game
from editor import Editor


class Application:
    """Classe rassemblant les différents éléments pour programme final."""

    def __init__(self):
        self.running = False
        self.events = Event("", None)
        self.height = 600
        self.width = 800
        self.fullscreen = False

    def run(self):
        """Fonction permettant de lancer le programme.

        Return None
        """
        self.running = True

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

        def play():
            plateau, nb_of_grass, entities = self.load_map()
            game = Game(entities, plateau, nb_of_grass,
                        main_events, save, self.events)

        def editor():
            edit = Editor(menu, load_map, savetxt, self.events)

        buttons.append(Button(25, 25, 40, 20, "Play", play))
        buttons.append(Button(25, 50, 40, 20, "Editor", editor))
        # buttons.append(Button(200, 250, 600, 350, "Random Map", play))

        while self.running:
            self.menu(buttons)
            fl.mise_a_jour()

        fl.ferme_fenetre()


    def menu(self, buttons):
        """Fonction permettant d'afficher certains boutons dans la fenetre.
        
        Return None"""
        fl.efface_tout()
        self.events.get_ev()
        if self.main_events(): return True

        for button in buttons:
            button.update(self.events)


    def main_events(self):
        """Fonction permettant de gérer les évènements nécessaire
        au bon fonctionnement du programme.

        Returns:
            bool: True si l'utilisateur veut quitter le programme, None sinon.
        """
        if self.events.type == "Quitte":
            self.running = False
            return True
        elif self.events.type == "Touche" and self.events.data == "F11":
            self.fullscreen = not self.fullscreen
            fl.set_fullscreen(self.fullscreen)
    
    
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
            with open(file_path, 'r') as f:
                for i, line in enumerate(f):
                    temp = []
                    for j, char in enumerate(line):
                        if char == '_':
                            temp.append(None)
                        elif char == 'S':
                            entities.append(Sheep(i, j))
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
                        entities.append(
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


app = Application()
app.run()
