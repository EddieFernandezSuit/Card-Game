import pygame
from entities.entity import Entity
from entities.text import TextHandler
from components.transform_component import TransformComponent
from Timer import Timer
import random
import math

class FlyingNum(Entity):
    def __init__(self, game, str, position, color) -> None:
        super().__init__(game)
        self.text = TextHandler(game, str, position, self.game.fonts["medium"])
        self.text.color = color
        self.text.transform_component.speed = 2
        self.text.transform_component.gravity = .05
        x_range =.5
        self.text.transform_component.direction = pygame.Vector2(random.uniform(-x_range, x_range), -1).normalize()


        self.timer = Timer(60, self.destroy)

    def update(self):
        self.timer.update()

    def destroy(self):
        self.text.delete()
        self.game.currentState['gameObjects'].remove(self)
        del self
