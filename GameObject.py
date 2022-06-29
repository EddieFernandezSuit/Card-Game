class GameObject:
    def __init__(self,game) -> None:
        game.gameObjects.append(self)
    
    def update(self):
        pass