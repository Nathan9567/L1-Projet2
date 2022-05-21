from event import Event


class Sheep:
    """Classe représentant un mouton sur le plateau"""

    def __init__(self, x: int, y: int, settings: dict) -> None:
        self.x = x
        self.y = y
        self.settings = settings
        self.sprite = "./media/sheep.png"

    def __eq__(self, other: object) -> bool:
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def add_to_dict(self, entities):
        """Ajoute le mouton dans le dictionnaire des entités"""
        entities[(self.x, self.y)] = entities.get((self.x, self.y), [])
        entities[(self.x, self.y)].append(self)

    def update(self, event: Event, map: list, entities: dict) -> None:
        """Mise à jour du mouton"""
        cmpt = 0
        if event.type == 'Touche':
            if event.data == self.settings['Up']:
                for x in range(self.x, 0, -1):
                    if map[self.x-1][self.y] != 'B':
                        self.x -= 1
                return self.add_to_dict(entities)
            elif event.data == self.settings['Down']:
                for x in range(self.x, len(map)-1):
                    if map[self.x+1][self.y] != 'B':
                        self.x +=1
                return self.add_to_dict(entities)
            elif event.data == self.settings['Left']:
                for y in range(self.y, 0, -1):
                    if map[self.x][self.y-1] != 'B':
                        self.y = self.y - 1
                return self.add_to_dict(entities)
            elif event.data == self.settings['Right']:
                for y in range(self.y, len(map[0])-1):
                    if map[self.x][self.y+1] != 'B':
                        self.y +=1
                return self.add_to_dict(entities)
            
                

        self.add_to_dict(entities)
