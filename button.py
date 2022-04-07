import fltk as fl
from event import Event
from types import FunctionType

class Button:
    """
    Classe representant et dessinant un bouton grace à la bibliothèque fltk permetde detecter les clics et de leur assigner une fonction"
    """

    def __init__(self, ax: int, ay: int, bx: int, by: int, text: str, function: FunctionType) -> None:
        """
        Initialisation des attributs du bouton et de la fonction à appeler
        """
        self.button = fl.rectangle(ax, ay, bx, by, couleur='grey', remplissage='grey', epaisseur=1, tag='')
        self.btn_text = fl.texte(ax+5, ay+5, text, couleur='black', ancrage='nw', police='Helvetica', taille=20, tag='')
        self.text = text
        self. ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.function = function


    def is_hovered(self) -> bool:
        """
        On vérifie les coordonnées du curseur pour savoir si il se trouve sur le bouton
        """
        souris = [ fl.abscisse_souris(), fl.ordonnee_souris()]
        if (souris[0] > self.ax and souris[0] < self.bx) and (souris[1] > self.ay and souris[1] < self.by):
            return True
        return False

    def update(self, event: Event) -> None:
        """
        Fonction à appeler chaque frame verifie les clics et met appelle la fonction si necessaire
        """
        if self.is_hovered():
            self.button = fl.rectangle(self.ax, self.ay, self.bx, self.by, couleur='grey', remplissage='red', epaisseur=1, tag='')
            self.btn_text = fl.texte(self.ax+5, self.ay+5, self.text, couleur='black', ancrage='nw', police='Helvetica', taille=20, tag='')
            if  event.type == 'ClicGauche':
                self.function()
        else:
            self.button = fl.rectangle(self.ax, self.ay, self.bx, self.by, couleur='grey', remplissage='grey', epaisseur=1, tag='')
            self.btn_text = fl.texte(self.ax+5, self.ay+5, self.text, couleur='black', ancrage='nw', police='Helvetica', taille=20, tag='')
            self.clicked = False

        fl.mise_a_jour()