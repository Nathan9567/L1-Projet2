from event import Event


class Sheep:
    """Classe représentant un mouton sur le plateau"""

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def update(self, event: Event, map: list) -> None:
        """Mise à jour du mouton"""
        allowed_cell = [None, 'G']
        if event.type == 'Touche':
            if event.data == 'Up' and map[self.x - 1][self.y] in allowed_cell:
                self.x = max(self.x - 1, 0)
            elif event.data == 'Down' and map[min(self.x + 1, len(map) - 1)][self.y] in allowed_cell:
                self.x = min(self.x + 1, len(map) - 1)
            elif event.data == 'Left' and map[self.x][self.y - 1] in allowed_cell:
                self.y = max(self.y - 1, 0)
            elif event.data == 'Right' and map[self.x][min(self.y + 1, len(map[0]) - 1)] in allowed_cell:
                self.y = min(self.y + 1, len(map[0]) - 1)
            print(self.x, self.y)
