import math
import pygame
from GameObjects.GameObject import GameObject
from GameObjects.Player import Player
from Handlers.ImageHandler import ImageHandler

class Arrow(GameObject):
    def __init__(self, game, originObject, targetObject) -> None:
        super().__init__(game)
        targetCenter = 0
        if (type(originObject) == Player):
            targetCenter = targetObject.textHandler.imageHandler.getCenter()
        else:
            targetCenter = targetObject.imageHandler.getCenter()
        self.imageHandler = ImageHandler('Images/arrow.jpg',pygame.Vector2(), game)
        self.position = originObject.imageHandler.getCenter() - self.imageHandler.getCenter()
        self.imageHandler.position = self.position
        self.targetPosition = targetCenter - self.imageHandler.getCenter()
        self.direction = (targetCenter- self.position).normalize()
        self.speed = 15
        self.imageHandler.setAngle(math.degrees(math.atan2(self.direction.x, self.direction.y)) + 180)
        self.targetRect = targetObject.imageHandler.getRect()
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