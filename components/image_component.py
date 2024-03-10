from entities.entity import Entity
import pygame
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path) 

class ImageComponent(Entity):
    def __init__(self, filePath, entity=None) -> None:
        super().__init__(entity.game)
        self.image = pygame.image.load(resource_path(filePath)).convert_alpha()
        self.entity = entity
        self.entity.transform_component.rect.width = self.image.get_rect().width
        self.entity.transform_component.rect.height = self.image.get_rect().height
        self.angle = 0
        
    def update(self):
        self.draw()

    def draw(self):
        self.game.screen.blit(self.image, self.entity.transform_component.position)
        
    def setAngle(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, self.angle)

    def getCenter(self):
        return pygame.Vector2(self.entity.transform_component.position.x + self.image.get_rect().width/2, self.entity.transform_component.position.y + self.image.get_rect().height/2)
