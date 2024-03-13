
import pygame
from entities.entity import Entity
from entities.text import TextHandler
from components.click_component import ClickComponent
import Colors

class ClickableText(Entity):
    def __init__(self, game, position, on_click, args, str, font):
        super().__init__(game)
        self.on_click = on_click
        self.textHandler = TextHandler(game, str, position, font)
        self.transform_component = self.textHandler.transform_component
        self.clickHandler = ClickComponent(args, self)
    
    def update(self):
        super().update()
        mouse_position = pygame.mouse.get_pos()
        self.textHandler.color = Colors.CYAN if self.transform_component.rect.collidepoint(pygame.Vector2(mouse_position)) else Colors.WHITE

    def delete(self):
        self.transform_component.delete()
        self.textHandler.delete()
        self.clickHandler.delete()
        return super().delete()

