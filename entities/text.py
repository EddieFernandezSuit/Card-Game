from requests import delete
import Colors
from Colors import *
import pygame

from entities.entity import Entity
from components.transform_component import TransformComponent


class TextHandler(Entity):
    def __init__(self, game, str, position, font) -> None:
        super().__init__(game)
        self.str = str
        self.font = font
        width, height = self.font.size(self.str)
        self.transform_component = TransformComponent(game, position, width=width, height=height)
        self.color = WHITE
        self.text_surface = self.font.render(self.str, 1 , self.color)
        self.visible = True

    def update(self):
        if self.visible:
            for i in range(4):
                outlineSize = 1
                outline_peice_surface = self.font.render(self.str, 1, Colors.BLACK)
                position = pygame.Vector2(self.transform_component.position.x + (i % 2 * 2 - 1) * outlineSize, self.transform_component.position.y + (i // 2 * 2 - 1) * outlineSize)
                self.game.screen.blit(outline_peice_surface, position)
            
            self.text_surface = self.font.render(self.str, 1 , self.color)
            self.game.screen.blit(self.text_surface, self.transform_component.position)

    def delete(self):
        self.game.currentState['gameObjects'].remove(self)