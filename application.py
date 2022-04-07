import fltk as fl
from event import Event
from button import Button 
from tkinter import filedialog


class Application:

    def __init__(self):
        self.entities = list()
        self.running = False
        self.events = Event("", None)

    
    def run(self):
        self.running = True
        
        # Ouvrir fentre
        fl.cree_fenetre(800, 600)

        # Bouttons/ Menu
        buttons = list()
        def play():
            self.play()
        buttons.append(Button(200, 250, 600, 350, "Play", play))

        while self.running:
            self.events.get_ev()
            if self.events.type == "Quitte":
                self.running = False
                break
            
            for button in buttons:
                button.update(selfevents)
            fl.mise_a_jour()
        fl.ferme_fenetre()
        

    def play(self):
        # ouvrir file dialog
        # peupler not table 'entities' avec le fichier

        #while self.running:
        #   on prend les inputs
        #   on affiche le background
        #   for entity in entities:
        #   entity.update()

        file_path = filedialog.askopenfilename()
        print(file_path)
        
app = Application()
app.run()