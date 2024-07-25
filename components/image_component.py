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
    def on_init(self, filePath=None, image=None, entity=None, visible=True) -> None:
        self.set_attributes(locals())
        if filePath: self.image = pygame.image.load(resource_path(filePath)).convert_alpha()
        self.position_offset = pygame.Vector2(0,0)

    def update(self):
        if self.visible:
            self.draw()
    
    def setup(self):
        self.image = pygame.transform.rotate(self.image, self.entity.transform_component.rotation)
        self.entity.transform_component.rect.size = self.image.get_rect().size

    def draw(self):
        self.game.screen.blit(self.image, self.entity.transform_component.position + self.position_offset)
    
    def set_rotation(self, angle):
        self.entity.transform_component.rotation = angle
        self.image = pygame.transform.rotate(self.image, self.entity.transform_component.rotation)
