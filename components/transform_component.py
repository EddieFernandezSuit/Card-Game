from entities.entity import Entity
import pygame

class TransformComponent(Entity):
    def __init__(self, game, position, width = 0, height = 0) -> None:
        super().__init__(game)
        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(0,0)
        self.speed = 0
        self.gravity = 0
        self.vSpeed = 0
        self.rect = pygame.Rect(self.position.x, self.position.y, width, height)

    def update(self):
        self.vSpeed += self.gravity
        self.position.y += self.vSpeed
        self.position += self.direction * self.speed
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        