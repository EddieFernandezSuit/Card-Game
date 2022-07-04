import math
from turtle import pos
import pygame
from GameObject import GameObject
from Handlers.ImageHandler import ImageHandler

class Arrow(GameObject):
    def __init__(self, game, position, destination, targetRect) -> None:
        super().__init__(game)
        self.game = game
        self.imageHandler = ImageHandler('Images/arrow.png',pygame.Vector2(), game)
        self.position = position - self.imageHandler.getCenter()
        self.imageHandler.position = self.position
        self.destination = destination - self.imageHandler.getCenter()
        self.direction = (destination - self.position).normalize()
        self.speed = 10
        self.imageHandler.setAngle(math.degrees(math.atan2(self.direction.x, self.direction.y)) + 180)
        self.targetRect = targetRect
        
    def update(self):
        self.position += self.direction * self.speed

        rect1 = self.imageHandler.image.get_rect()
        rect1.x += self.imageHandler.position.x
        rect1.y += self.imageHandler.position.y


        print(rect1.colliderect(self.targetRect))
        if(rect1.colliderect(self.targetRect)):
            self.delete()

    def delete(self):
        self.game.gameObjects.remove(self)
        self.game.gameObjects.remove(self.imageHandler)
