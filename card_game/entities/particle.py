
import pygame
from card_game.entities.entity import Entity
from card_game.components.transform_component import TransformComponent
from card_game.core.constants import *
from card_game.core.timer import Timer

class Particle(Entity):
    def __init__(self, game, position, direction = (0,1)) -> None:
        super().__init__(game)
        self.add_components(TransformComponent(game, pygame.Vector2(position), uniform_size=3, speed=.6, direction=(direction)))
        self.timer = Timer(30, self.delete)

    def update(self):
        self.timer.update()
        pygame.draw.circle(self.game.screen, CYAN, self.transform_component.position, self.transform_component.rect.width)
