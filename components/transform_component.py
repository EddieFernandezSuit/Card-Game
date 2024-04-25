from entities.entity import Entity
import pygame

class TransformComponent(Entity):
    def on_init(self, position=(0,0), width = 0, height = 0, size=None, uniform_size=None, speed = 0, rotation=0, direction=pygame.Vector2(0,0)):
        self.__dict__.update(locals())
        self.position = pygame.Vector2(position)
        if size: width, height = size
        if uniform_size: width, height = uniform_size, uniform_size
        self.rect = pygame.Rect(self.position.x, self.position.y, width, height)
        self.gravity = 0
        self.dy = 0

    def update(self):
        self.dy += self.gravity
        self.position.y += self.dy
        self.position += self.direction * self.speed
        self.rect.topleft = self.position
    
    def set_attributes(self, speed=0, gravity=0, direction=pygame.Vector2(0,0)):
        self.speed = speed
        self.gravity = gravity
        self.direction = direction