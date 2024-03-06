
import pygame
from GameObjects.GameObject import GameObject
from Handlers.TransformHandler import TransformHandler
import Colors
from Timer import Timer
import random

class Particle(GameObject):
    def __init__(self, game, position) -> None:
        super().__init__(game)
        self.transformHandler = TransformHandler(game, pygame.Vector2(position))
        self.transformHandler.speed = 1
        self.transformHandler.direction = pygame.Vector2(0,-1)
        self.timer = Timer(100, self.delete)

    def update(self):
        self.game.screen.set_at((int(self.transformHandler.position.x) + random.randint(0,200), int(self.transformHandler.position.y)), Colors.GREEN)
        self.timer.update()

    def delete(self):
        self.game.currentState.remove(self)