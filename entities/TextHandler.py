from requests import delete
import Colors
from Colors import *
import pygame

from entities.entity import Entity
from components.transform_component import TransformComponent


class TextHandler(Entity):
    def __init__(self, game, str, basePosition, positionOffset, font) -> None:
        super().__init__(game)
        self.str = str
        self.game = game
        self.basePosition = basePosition
        self.positionOffset = positionOffset
        self.font = font
        self.width, self.height = self.font.size(self.str)
        self.transform_component = TransformComponent(game, self.basePosition + self.positionOffset, width=self.width, height=self.height)
        self.color = WHITE
        self.text_surface = self.font.render(self.str, 1 , self.color)

    def update(self):
        self.transform_component.position = self.basePosition + self.positionOffset

        for i in range(4):
            outlineSize = 1
            outline_peice_surface = self.font.render(self.str, 1, Colors.BLACK)
            position = pygame.Vector2(self.transform_component.position.x + (i % 2 * 2 - 1) * outlineSize, self.transform_component.position.y + (i // 2 * 2 - 1) * outlineSize)
            self.game.screen.blit(outline_peice_surface, position)
        
        self.text_surface = self.font.render(self.str, 1 , self.color)
        self.game.screen.blit(self.text_surface, self.transform_component.position)

    def delete(self):
        self.game.currentState['gameObjects'].remove(self)
    
    def getCenter(self):
        return pygame.Vector2(self.transform_component.position.x + self.text_surface.get_rect().width/2, self.transform_component.position.y + self.text_surface.get_rect().height/2)