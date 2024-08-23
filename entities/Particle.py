
import pygame
from entities.entity import Entity
from components.transform_component import TransformComponent
from constants import *
from Timer import Timer

class Particle(Entity):
    def __init__(self, game, position, direction = (0,1)) -> None:
        super().__init__(game)
        self.transformHandler = TransformComponent(game, pygame.Vector2(position), uniform_size=3, speed=.6, direction=(direction))
        self.timer = Timer(30, self.delete)

    def update(self):
        self.timer.update()
        pygame.draw.circle(self.game.screen, CYAN, self.transformHandler.position, self.transformHandler.rect.width)
