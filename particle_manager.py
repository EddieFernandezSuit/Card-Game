import random
from entities.particle import Particle

class ParticleManager:
    def __init__(self, game) -> None:
        self.game = game
    
    def update(self):
        turn = self.game.currentState['turn']
        x = random.random() * self.game.SCREEN_WIDTH
        y = self.game.SCREEN_HEIGHT * turn
        position = (x,y)
        direction = (0, 1 - (2 * turn))

        Particle(self.game, position, direction)