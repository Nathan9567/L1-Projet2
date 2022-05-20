import fltk as fl
from event import Event
from types import FunctionType


class Button:
    """
    Classe representant et dessinant un bouton grace à la bibliothèque fltk permetde detecter les clics et de leur assigner une fonction"
    """

    def __init__(self, x: int, y: int, width: int, height: int, text: str, function: FunctionType, arg: any=None) -> None:
        """
        Initialisation des attributs du bouton et de la fonction à appeler
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.new_x = int(self.x / 100 * fl.get_width())
        self.new_y = int(self.y / 100 * fl.get_height())
        self.new_width = int(self.width / 100 * fl.get_width())
        self.new_height = int(self.height / 100 * fl.get_height())
        self.button = fl.rectangle(
            self.new_x, self.new_y, self.new_x + self.new_width, self.new_y + self.new_height, couleur='grey', remplissage='grey', epaisseur=1, tag='')
        self.text = text
        self.function = function
        self.arg = arg

    def is_hovered(self) -> bool:
        """
        On vérifie les coordonnées du curseur pour savoir si il se trouve sur le bouton
        """
        souris = [fl.abscisse_souris(), fl.ordonnee_souris()]
        if (souris[0] > self.new_x and souris[0] < self.new_x + self.new_width) and (souris[1] > self.new_y and souris[1] < self.new_y + self.new_height):
            return True
        return False

    def update(self, event: Event) -> any:
        """
        Fonction à appeler chaque frame verifie les clics et met appelle la fonction si necessaire
        """
        textx, texty = fl.taille_texte(
            self.text, taille=20)
        self.new_x = int(self.x / 100 * fl.get_width())
        self.new_y = int(self.y / 100 * fl.get_height())
        self.new_width = int(self.width / 100 * fl.get_width())
        self.new_height = int(self.height / 100 * fl.get_height())
        if self.is_hovered():
            self.button = fl.rectangle(
                self.new_x, self.new_y, self.new_x + self.new_width, self.new_y + self.new_height, couleur='grey', remplissage='red', epaisseur=1, tag='')
            self.btn_text = fl.texte(self.new_x + self.new_width - (self.new_x + self.new_width - self.new_x)/2 - textx/2, self.new_y + self.new_height - (self.new_y + self.new_height - self.new_y)/2 - texty/2, self.text, couleur='black',
                                     ancrage='nw', police='Helvetica', taille=20, tag='')
            if event.type == 'ClicGauche':
                if self.arg is None:
                    return self.function()
                else:
                    return self.function(self.arg)
        else:
            self.button = fl.rectangle(
                self.new_x, self.new_y, self.new_x + self.new_width, self.new_y + self.new_height, couleur='grey', remplissage='grey', epaisseur=1, tag='')
            self.btn_text = fl.texte(self.new_x + self.new_width - (self.new_x + self.new_width - self.new_x)/2 - textx/2, self.new_y + self.new_height - (self.new_y + self.new_height - self.new_y)/2 - texty/2, self.text, couleur='black',
                                     ancrage='nw', police='Helvetica', taille=20, tag='')
            self.clicked = False
