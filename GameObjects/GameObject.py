class GameObject:
    def __init__(self, game) -> None:
        self.game = game
        game.currentState['gameObjects'].append(self)
    
    def update(self):
        pass
    
    def delete(self):
        self.game.currentState['gameObjects'].remove(self)
        del(self)