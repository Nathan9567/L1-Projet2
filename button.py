import fltk as fl
from event import Event
from types import FunctionType


class Button:
    """
    Classe representant et dessinant un bouton grace à la bibliothèque fltk permetde detecter les clics et de leur assigner une fonction"
    """

    def __init__(self, x: int, y: int, width: int, height: int, text: str, function: FunctionType, *args: any) -> None:
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
        self.args = args

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
            self.text, taille = self.get_text_size())
        self.new_x = int(self.x / 100 * fl.get_width())
        self.new_y = int(self.y / 100 * fl.get_height())
        self.new_width = int(self.width / 100 * fl.get_width())
        self.new_height = int(self.height / 100 * fl.get_height())
        if self.is_hovered():
            self.button = fl.rectangle(
                self.new_x, self.new_y, self.new_x + self.new_width, self.new_y + self.new_height, couleur='grey', remplissage='red', epaisseur=1, tag='')
            self.btn_text = fl.texte(self.new_x + self.new_width - (self.new_x + self.new_width - self.new_x)/2 - textx/2, self.new_y + self.new_height - (self.new_y + self.new_height - self.new_y)/2 - texty/2, self.text, couleur='black',
                                     ancrage='nw', police='Helvetica', taille=self.get_text_size(), tag='')
            if event.type == 'ClicGauche':
                return self.function(*self.args)
        else:
            self.button = fl.rectangle(
                self.new_x, self.new_y, self.new_x + self.new_width, self.new_y + self.new_height, couleur='grey', remplissage='grey', epaisseur=1, tag='')
            self.btn_text = fl.texte(self.new_x + self.new_width - (self.new_x + self.new_width - self.new_x)/2 - textx/2, self.new_y + self.new_height - (self.new_y + self.new_height - self.new_y)/2 - texty/2, self.text, couleur='black',
                                     ancrage='nw', police='Helvetica', taille=self.get_text_size(), tag='')
            self.clicked = False

    def get_text_size(self):
        """Permet de récupérer la taille du texte

        Returns:
            int: taille du texte
        """
        return int(self.height / 100 * fl.get_height() * 0.5)
