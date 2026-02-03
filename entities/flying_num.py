import pygame
from entities.entity import Entity
from entities.text import Text
from Timer import Timer
import random

class FlyingNum(Entity):
    def on_init(self, str, position, color) -> None:
        self.timer = None
        self.time = 140
        self.text = Text(self.game, str, position, font_size='small', color=color)
        x_range =.2
        self.transform_component = self.text.transform_component
        self.transform_component.set_attributes(speed=1.1, gravity=0.01, direction=pygame.Vector2(random.uniform(-x_range, x_range), -1).normalize())
        self.timer = Timer(self.time, self.delete)

    def update(self):
        if self.timer:
            self.timer.update()

    def on_delete(self):
        self.timer = None
        self.text.delete()