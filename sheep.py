from event import Event


class Sheep:
    """Classe représentant un mouton sur le plateau"""

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.sprite = "./media/sheep.png"

    def update(self, event: Event, map: list) -> None:
        """Mise à jour du mouton"""
        allowed_cell = [None, 'G']
        if event.type == 'Touche':
            while True:
                if event.data == 'Up' and map[self.x - 1][self.y] in allowed_cell:
                    self.x = max(self.x - 1, 0)
                    if self.x == 0:
                        break
                elif event.data == 'Down' and map[min(self.x + 1, len(map) - 1)][self.y] in allowed_cell:
                    self.x = min(self.x + 1, len(map) - 1)
                    if self.x == len(map) - 1:
                        break
                elif event.data == 'Left' and map[self.x][self.y - 1] in allowed_cell:
                    self.y = max(self.y - 1, 0)
                    if self.y == 0:
                        break
                elif event.data == 'Right' and map[self.x][min(self.y + 1, len(map[0]) - 1)] in allowed_cell:
                    self.y = min(self.y + 1, len(map[0]) - 1)
                    if self.y == len(map[0]) - 1:
                        break
                else:
                    break
        if map[self.x][self.y] == 'G':
            self.sprite = "./media/sheep_grass.png"
        else:
            self.sprite = "./media/sheep.png"
        # print(self.x, self.y)
