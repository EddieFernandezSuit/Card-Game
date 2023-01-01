class GameObject:
    def __init__(self,game) -> None:
        self.game = game
        game.states[game.currentState]['gameObjects'].append(self)
    
    def update(self):
        pass
    
    def delete(self):
        self.game.states[self.game.currentState].remove(self)
        del(self)