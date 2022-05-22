import fltk as fl
from event import Event
from button import Button
from types import FunctionType


class Editor:
    """Classe permettant l'édition et la création d'un plateau.
    """
    def __init__(self, menu: FunctionType, load: FunctionType,
                 save: FunctionType, events: Event, settings: dict,
                 screensize: FunctionType):
        """Constructeur de l'éditeur.

        Args:
            menu (FunctionType): Fonction permettant de créer le menu
            load (FunctionType): Fonction permettant de charger un plateau
            save (FunctionType): Fonction permettant de sauvegarder un plateau
            events (Event): Objet permettant de gérer les évènements
        """
        self.plateau = list()
        self.load = load
        self.editing = [False, False]
        self.selected = None
        self.save = save
        self.events = events
        self.menu = menu
        self.plateau = []
        self.sprites = {'B': './media/bush.png', 'G': './media/grass.png',
                        'S': './media/sheep.png'}
        self.settings = settings
        self.is_screensize_changed = screensize
        self.editor()

    def editor(self):
        """Fonction permettant de créer le premier menu de l'éditeur.
        Avec le chargement ou la création d'un plateau.

        Return None
        """
        fl.efface_tout()
        self.editing[0] = True
        edit_buttons = []
        self.background = False

        def load():
            self.background = False
            self.plateau, _, entities = self.load()
            for entity in entities:
                self.plateau[entity.x][entity.y] = 'S'
            if self.plateau == []:
                return None
            self.editing[1] = True
            self.edit()

        def back():
            self.background = False
            self.editing[0] = False

        def new():
            self.background = False
            dimensions_str = fl.get_user_input(
                "Taille", "Entrez les dimensions du plateau "
                "(en nombre de cases): largeur:hauteur")
            dimensions = [0, 0]
            try:
                dimensions[0] = int(dimensions_str.split(':')[0])
                dimensions[1] = int(dimensions_str.split(':')[1])
            except:
                return None
            self.plateau = [[None for _ in range(dimensions[0])]
                            for _ in range(dimensions[1])]
            self.editing[1] = True
            self.edit()
            

        edit_buttons.append(Button(0, 0, 33, 5, 'Back', back))
        edit_buttons.append(Button(33, 0, 34, 5, 'Load', load))
        edit_buttons.append(Button(67, 0, 33, 5, 'New', new))
        
        self.plateau = [[None for _ in range(5)] for _ in range(5)]
        self.render()
        while self.editing[0]:
            fl.efface('b')
            if self.is_screensize_changed() or not self.background:
                self.plateau = [[None for _ in range(5)] for _ in range(5)]
                self.render()
                self.background = True
            if self.menu(edit_buttons):
                return None
            if self.events.type == "Touche":
                if self.events.data == self.settings['Back']:
                    self.editing[0] = False
            fl.mise_a_jour()

    def edit(self):
        """Fonction permettant l'execution de l'édition du plateau.
        Créer les boutons permettant la selection des différents éléments
        et leur placement.

        Return None
        """
        fl.efface_tout()
        editing_buttons = []

        def items(item):
            self.selected = item

        def back():
            self.editing[1] = False
        editing_buttons.append(Button(0, 0, 20, 5, 'Back', back))
        editing_buttons.append(Button(20, 0, 20, 5, 'Save', self.save,
                                      self.plateau))
        editing_buttons.append(Button(40, 0, 20, 5, 'Sheep', items, 'S'))
        editing_buttons.append(Button(60, 0, 20, 5, 'Grass', items, 'G'))
        editing_buttons.append(Button(80, 0, 20, 5, 'Bush', items, 'B'))
        self.render()
        while self.editing[1]:
            # print(self.events.type)
            if self.menu(editing_buttons):
                self.editing[0] = False
                return None
            if self.events.type == "Touche":
                if self.events.data == self.settings['Back']:
                    self.editing[1] = False
            if fl.ordonnee_souris() > fl.get_height()*0.05:
                if self.events.type == "ClicGauche":
                    x, y = self.clicked_box((fl.abscisse_souris(),
                                             fl.ordonnee_souris()))
                    self.plateau[y][x] = self.selected
                    self.render()
                if self.events.type == "ClicDroit":
                    x, y = self.clicked_box((fl.abscisse_souris(),
                                             fl.ordonnee_souris()))
                    self.plateau[y][x] = None
                    self.render()
            if self.is_screensize_changed():
                self.render()
            fl.mise_a_jour()

    def render(self):
        """Fonction permettant de dessiner le plateau dans
        la fenetre de l'éditeur.

        Return None
        """
        fl.efface_tout()
        x, y = len(self.plateau), len(self.plateau[0])
        window_h = fl.get_height()
        w, h = fl.get_width(), window_h*0.95
        fl.rectangle(0, h*0.05, fl.get_width(),
                     fl.get_height(), remplissage='#e0e0e0')
        fl.image(0, h*0.05, fl.get_width(), fl.get_height(),
                 './media/background/gazon.png', ancrage='sw')

        for i in range(x):
            fl.ligne(0, h/x*i + h*0.05, w, h/x*i + h*0.05)
        for i in range(y):
            fl.ligne(w/y*i, h*0.05, w/y*i, window_h)

        for px in range(len(self.plateau)):
            for py in range(len(self.plateau[0])):
                if self.plateau[px][py] is not None:
                    fl.image(w/y*py, h/x*px + h*0.05, w/y *
                             (py + 1), h/x*(px + 1) + h*0.05,
                             self.sprites[self.plateau[px][py]], ancrage='sw')

    def clicked_box(self, souris):
        """Fonctio détectant la case cliquée avec la souris.

        Args:
            souris (tuple(int)): coordonnées (x, y) de la souris

        Returns:
            tuple(int): coordonnées (x, y) de la case cliquée
        """
        x, y = len(self.plateau), len(self.plateau[0])
        window_h = fl.get_height()
        w, h = fl.get_width(), window_h*0.95
        box_x = int(souris[0]/w * y)
        box_y = int((souris[1]-window_h*0.05)/h * x)
        return (box_x, box_y)
