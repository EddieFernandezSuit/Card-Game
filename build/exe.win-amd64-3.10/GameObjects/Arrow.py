import math
import pygame
from GameObjects.GameObject import GameObject
from Handlers.ImageHandler import ImageHandler

class Arrow(GameObject):
    def __init__(self, game, origionPosition, destinationPosition, targetRect, originHealthObject, targetHealthObject) -> None:
        super().__init__(game)
        self.game = game
        self.imageHandler = ImageHandler('Images/arrow.jpg',pygame.Vector2(), game)
        self.position = origionPosition - self.imageHandler.getCenter()
        self.imageHandler.position = self.position
        self.destination = destinationPosition - self.imageHandler.getCenter()
        self.direction = (destinationPosition - self.position).normalize()
        self.speed = 15
        self.imageHandler.setAngle(math.degrees(math.atan2(self.direction.x, self.direction.y)) + 180)
        self.targetRect = targetRect
        self.originHealthObject = originHealthObject
        self.targetHealthObject = targetHealthObject

    def update(self):
        self.position += self.direction * self.speed
        arrowRect = self.imageHandler.getRect()

        if(arrowRect.colliderect(self.targetRect)):
            self.originHealthObject.dealDamage(self.targetHealthObject)
            self.delete()

    def delete(self):
        self.game.gameObjects.remove(self)
        self.game.gameObjects.remove(self.imageHandler)