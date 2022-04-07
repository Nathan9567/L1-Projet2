from event import Event

class Sheep:
    """Classe représentant un mouton sur le plateau"""
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def update(self, event: Event) -> None:
        """Mise à jour du mouton"""
        if event.type == 'Touche':
            if event.data == 'Up':
                self.y -= 1
            elif event.data == 'Down':
                self.y += 1
            elif event.data == 'Left':
                self.x -= 1
            elif event.data == 'Right':
                self.x += 1