import pygame
from entities.entity import Entity
from entities.text import Text
from Timer import Timer
import random

class FlyingNum(Entity):
    def on_init(self, str, position, color) -> None:
        self.timer = None
        self.text = Text(self.game, str, position, color=color)
        x_range =.5
        self.transform_component = self.text.transform_component
        self.transform_component.set_attributes(speed=1.9, gravity=0.04, direction=pygame.Vector2(random.uniform(-x_range, x_range), -1).normalize())
        self.timer = Timer(80, self.delete)

    def update(self):
        if self.timer:
            self.timer.update()

    def on_delete(self):
        self.timer = None
        self.text.delete()