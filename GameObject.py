class GameObject:
    def __init__(self,game) -> None:
        self.game = game
        game.gameObjects.append(self)
    
    def update(self):
        pass