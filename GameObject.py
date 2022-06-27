

from logging import handlers


class GameObject:
    def __init__(self,game) -> None:
        game.gameObjects.append(self)
        self.handlers = []
    
    def update(self):
        for handler in self.handlers:
            handler.update()