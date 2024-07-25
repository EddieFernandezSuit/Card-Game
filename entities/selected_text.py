from entities.text import Text
from entities.entity import Entity
import pygame

class TextSelector(Entity):
    def on_init(self):
        self.text = Text(self.game, 'X')

    def update(self):
        self.text.visible = self.game.currentState['selectedCard'] is not None

        if self.game.currentState['selectedCard']:
            self.text.transform_component.position = pygame.Vector2(self.game.currentState['selectedCard'].transform_component.rect.center)
