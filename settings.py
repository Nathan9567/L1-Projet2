import fltk as fl
import os

from button import Button
from event import Event
from types import FunctionType


class Settings:
    """Classe permettant de gérer les paramètres du jeu"""

    def __init__(self, menu: FunctionType, events: Event, settings_dict: dict,
                 screensize: FunctionType):
        self.menu = menu
        self.events = events
        self.in_settings = False
        self.settings_dict = settings_dict
        self.selected = None
        self.is_screensize_changed = screensize

    def settings(self):
        fl.efface_tout()
        self.in_settings = True
        settings_buttons = list()

        def back():
            self.in_settings = False

        def set_settings(choice):
            self.selected = choice

        def create_buttons(dict):
            i = 0
            settings_buttons.append(Button(2, 2, 15, 10, "Back", back))
            for item in dict.items():
                settings_buttons.append(Button(50, 17+(i*8), 15, 7, item[1],
                                               set_settings, item[0]))
                i += 1

        self.render()
        create_buttons(self.settings_dict)
        while self.in_settings:
            if self.menu(settings_buttons):
                return None
            if self.events.type == "Touche":
                if self.events.data == self.settings_dict['Back']:
                    back()
            if self.selected is not None:
                temp = self.settings_dict.copy()
                temp[self.selected] = "..."
                settings_buttons = list()
                create_buttons(temp)
                for button in settings_buttons:
                    button.update(self.events)
                if self.events.type == 'Touche':
                    if self.events.data not in self.settings_dict.values():
                        self.settings_dict[self.selected] = self.events.data
                    self.selected = None
                    settings_buttons = list()
                    create_buttons(self.settings_dict)
                    fl.efface_tout()
                    self.render()
            if self.is_screensize_changed():
                fl.efface_tout()
                self.render()
            fl.mise_a_jour()

    def percent_text(self, x, y, text, couleur='black', taille_text=20,
                     epaisseur='1', underline=False, ancrage='center'):
        taille = fl.taille_texte(text, police='Helvetica',
                                 taille=taille_text)
        fl.texte(x/100 * fl.get_width(), y/100 * fl.get_height(),
                 chaine=text, couleur=couleur, ancrage=ancrage,
                 police='Helvetica', taille=taille_text)
        if underline:
            fl.ligne(x/100 * fl.get_width() - taille[0]/2,
                     y/100 * fl.get_height() + taille[1]/2,
                     x/100 * fl.get_width() + taille[0]/2,
                     y/100 * fl.get_height() + taille[1]/2,
                     couleur=couleur, epaisseur=epaisseur)

    def render(self):
        fl.image(0, 0, fl.get_width(), fl.get_height(),
        "media/background/settings.png", ancrage='sw')
        j = 0
        for key in self.settings_dict:
            self.percent_text(5, 17+(j*8), key, couleur='black',
                              taille_text=20, ancrage='nw')
            j += 1
        self.percent_text(50, 5, "Settings :", couleur='black', taille_text=28,
                          epaisseur='2', underline=True)
        self.percent_text(50, 10, "Keys :", couleur='black', taille_text=20,
                          ancrage='nw')

    def get_settings(self):
        return self.settings_dict
    
    def save_settings(self):
        with open("settings.txt", "w") as f:
            for key, value in self.settings_dict.items():
                f.write(f"{key}:{value}\n")
    
    def import_settings(self):
        if not os.path.isfile('settings.txt'):
            self.save_settings()
            return None
        with open("settings.txt", "r") as f:
            for line in f:
                line = line.split(":")
                self.settings_dict[line[0]] = line[1].strip()
