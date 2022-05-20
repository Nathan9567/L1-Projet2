from event import Event


class Sheep:
    """Classe représentant un mouton sur le plateau"""

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.sprite = "./media/sheep.png"

    def __eq__(self, other: object) -> bool:
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def update(self, event: Event, map: list) -> None:
        """Mise à jour du mouton"""
        cmpt = 0
        if event.type == 'Touche':
            if event.data == 'Up':
                for x in range(self.x, 0, -1):
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
                        self.x = (x - cmpt) - 1
                        return None
                self.x = (len(map) - 1 - cmpt)
            elif event.data == 'Left':
                for y in range(self.y, 0, -1):
                    if map[self.x][y] == 'S':
                        cmpt += 1
                    if map[self.x][y] == 'B':
                        self.y = (y + cmpt) + 1
                        return None
                self.y = cmpt
            elif event.data == 'Right':
                for y in range(self.y, len(map[0])-1):
                    if map[self.x][y] == 'S':
                        cmpt += 1
                    if map[self.x][y] == 'B':
                        self.y = (y - cmpt) - 1 
                        return None
                self.y = (len(map[0]) - 1 - cmpt)
            else:
                return None

        print(self.x, self.y)
