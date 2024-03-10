import pygame
from entities.entity import Entity

class ClickComponent(Entity):
    def __init__(self, args, entity=None):
        super().__init__(entity.game)
        self.lastClick = 0
        self.args = args
        self.entity = entity
    
    def update(self):
        if pygame.mouse.get_pressed()[0] and self.lastClick == 0 and self.entity.transform_component.rect.collidepoint(pygame.mouse.get_pos()):
            self.entity.on_click(*self.args)
        self.lastClick = pygame.mouse.get_pressed()[0]
