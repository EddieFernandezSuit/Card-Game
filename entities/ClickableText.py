
import pygame
from entities.entity import Entity
from components.transform_component import TransformComponent
from entities.TextHandler import TextHandler
from components.click_component import ClickComponent
import Colors

class ClickableText(Entity):
    def __init__(self, game, position, on_click, args, str, font):
        super().__init__(game)
        self.on_click = on_click
        self.transform_component = TransformComponent(game, pygame.Vector2(position))
        self.textHandler = TextHandler(game, str, self.transform_component.position, pygame.Vector2(0,0), font)
        self.transform_component.rect = self.textHandler.transform_component.rect
        self.clickHandler = ClickComponent(args, self)
    
    def update(self):
        super().update()
        mouse_position = pygame.mouse.get_pos()
        if self.textHandler.transform_component.rect.collidepoint(pygame.Vector2(mouse_position)):
            self.textHandler.color = Colors.CYAN
        else:
            self.textHandler.color = Colors.WHITE

    def delete(self):
        self.transform_component.delete()
        self.textHandler.delete()
        self.clickHandler.delete()
        return super().delete()

