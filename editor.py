import fltk as fl
from event import Event
from button import Button
from types import FunctionType


class Editor:
    def __init__(self, menu: FunctionType, load: FunctionType, save: FunctionType, events: Event):
        self.plateau = list()
        self.load = load
        self.editing = False
        self.selected = None
        self.save = save
        self.events = events
        self.menu = menu
        self.plateau = []
        self.sprites = {'B': './media/bush.png', 'G': './media/grass.png',
                        'S': './media/sheep.png'}
        self.editor()
    
    def editor(self):
        fl.efface_tout()
        self.editing = True
        edit_buttons = []
        def load():
            self.plateau, _, entities = self.load()
            for entity in entities:
                self.plateau[entity.x][entity.y] = 'S'
            if self.plateau == []:
                return None
            self.edit()

        def back():
            self.editing = False
        def new():
            dimensions_str = fl.get_user_input("Taille", "Entrez les dimensions du plateau (en nombre de cases): largeur:hauteur")
            dimensions = [0, 0]
            dimensions[0] = int(dimensions_str.split(':')[0])
            dimensions[1] = int(dimensions_str.split(':')[1])
            self.plateau = [ [None for _ in range(dimensions[0])] for _ in range(dimensions[1])] 
            self.edit()
            pass
        edit_buttons.append(Button(0, 0, 33, 5, 'Back', back))
        edit_buttons.append(Button(33, 0, 34, 5, 'Load', load))
        edit_buttons.append(Button(67, 0, 33, 5, 'New', new))
        
        while self.editing:
            if self.menu(edit_buttons):
                return None
            fl.mise_a_jour()


    def edit(self):
        editing_buttons = []
        def items(item):
            self.selected = item
        def back():
            self.editing = False
        editing_buttons.append(Button(0, 0, 20, 5, 'Back', back))
        editing_buttons.append(Button(20, 0, 20, 5, 'Save', self.save, self.plateau))
        editing_buttons.append(Button(80, 0, 20, 5, 'Bush', items, 'B'))
        editing_buttons.append(Button(40, 0, 20, 5, 'Sheep', items, 'S'))
        editing_buttons.append(Button(60, 0, 20, 5, 'Grass', items, 'G'))
        while self.editing:
            if self.menu(editing_buttons):
                return None
            if self.events.type == "ClicGauche" and fl.ordonnee_souris() > fl.get_height()*0.05:
                x, y = self.clicked_box((fl.abscisse_souris(), fl.ordonnee_souris()))
                self.plateau[y][x] = self.selected
            if self.events.type == "ClicDroit" and fl.ordonnee_souris() > fl.get_height()*0.05:
                x, y = self.clicked_box((fl.abscisse_souris(), fl.ordonnee_souris()))
                self.plateau[y][x] = None
            self.render()
            fl.mise_a_jour()
            

    def render(self):
        x, y = len(self.plateau), len(self.plateau[0])
        window_h = fl.get_height()
        w, h = fl.get_width(), window_h*0.95
        fl.rectangle(0, h*0.05, fl.get_width(),
                     fl.get_height(), remplissage='#e0e0e0')
        # fl.image(0, h*0.05, fl.get_width(), fl.get_height(),
        #          './media/background.png', ancrage='sw')

        for i in range(x):
            fl.ligne(0, h/x*i+ h*0.05, w, h/x*i + h*0.05)
        for i in range(y):
            fl.ligne(w/y*i, h*0.05, w/y*i, window_h)

        for px in range(len(self.plateau)):
            for py in range(len(self.plateau[0])):
                if self.plateau[px][py] is not None:
                    fl.image(w/y*py, h/x*px+ h*0.05, w/y *
                             (py + 1), h/x*(px + 1) + h*0.05, self.sprites[self.plateau[px][py]], ancrage='sw')

    
    def clicked_box(self, souris):
        x, y = len(self.plateau), len(self.plateau[0])
        window_h = fl.get_height()
        w, h = fl.get_width(), window_h*0.95
        box_x = int(souris[0]/w * x)
        box_y = int((souris[1]-window_h*0.05)/h * y)
        return (box_x, box_y)
