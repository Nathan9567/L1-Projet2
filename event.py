import fltk as fl


class Event:
    """
    Classe permettant de représenter un evenement, pour permettre aux différentes classes de communiquer entre-elles
    Evite ainsi d'inclure une bibliothèque dans un fichier qui n'est pas fait pour cela
    """

    def __init__(self, type: str, data: any):
        self.type = type
        self.data = data

    def get_ev(self):
        self.ev = fl.donne_ev()
        self.type = fl.type_ev(self.ev)
        if self.type == 'Touche':
            self.data = fl.touche(self.ev)
