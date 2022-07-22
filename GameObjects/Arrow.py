import math
import pygame
from GameObjects.GameObject import GameObject
from Handlers.ImageHandler import ImageHandler

class Arrow(GameObject):
    def __init__(self, game, originObject, targetObject, originImg, targetImg) -> None:
        super().__init__(game)
        self.imageHandler = ImageHandler('Images/arrow.jpg',pygame.Vector2(), game)
        self.position = originImg.getCenter() - self.imageHandler.getCenter()
        self.imageHandler.position = self.position
        self.targetPosition = targetImg.getCenter() - self.imageHandler.getCenter()
        self.direction = (targetImg.getCenter() - self.position).normalize()
        self.speed = 15
        self.imageHandler.setAngle(math.degrees(math.atan2(self.direction.x, self.direction.y)) + 180)
        self.targetRect = targetImg.getRect()
        self.originObject = originObject
        self.targetObject = targetObject

    def update(self):
        self.position += self.direction * self.speed
        arrowRect = self.imageHandler.getRect()

        if(arrowRect.colliderect(self.targetRect)):
            self.originObject.dealDamage(self.targetObject)
            self.delete()

    def delete(self):
        self.game.arrowFlies = 0
        self.game.gameObjects.remove(self)
        self.game.gameObjects.remove(self.imageHandler)