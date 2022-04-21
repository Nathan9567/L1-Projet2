from event import Event


class Sheep:
    """Classe représentant un mouton sur le plateau"""

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.sprite = "./media/sheep.png"

    def update(self, event: Event, map: list, entities: list) -> None:
        """Mise à jour du mouton"""
        cmpt = 0
        if event.type == 'Touche':
            if event.data == 'Up':
                for x in reversed(range(0, self.x)):
                    if map[x][self.y] == 'S':
                        cmpt += 1
                    if map[x][self.y] == 'B':
                        self.x = (x + cmpt) + 1
                        return None
                self.x = cmpt
            elif event.data == 'Down':
                for x in range(self.x, len(map)):
                    if map[x][self.y] == 'S':
                        cmpt += 1
                    if map[x][self.y] == 'B':
                        self.x = (x - cmpt)
                        return None
                self.x = (len(map) - cmpt)
            elif event.data == 'Left':
                for y in reversed(range(0, self.y)):
                    if map[self.x][y] == 'S':
                        cmpt += 1
                    if map[self.x][y] == 'B':
                        self.y = (y + cmpt) + 1
                        return None
                self.y = cmpt
            elif event.data == 'Right':
                for y in range(self.y, len(map[0])):
                    if map[self.x][y] == 'S':
                        cmpt += 1
                    if map[self.x][y] == 'B':
                        self.y = (y - cmpt)
                        return None
                self.y = (len(map[0]) - cmpt)
            else:
                return None

        # print(self.x, self.y)
