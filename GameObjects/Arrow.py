from asyncio.windows_events import NULL
import math
import pygame
from GameObjects.GameObject import GameObject
from Handlers.ImageHandler import ImageHandler
from Handlers.TransformHandler import TransformHandler

class Arrow(GameObject):
    def __init__(self, game, originObject, targetObject) -> None:
        super().__init__(game)
        targetCenter = 0
        self.targetImageHandler = 0
        if (type(originObject) != type(targetObject)):
            self.targetImageHandler = targetObject.healthText.imageHandler
        else:
            self.targetImageHandler = targetObject.imageHandler
        targetCenter = self.targetImageHandler.getCenter()

        self.imageHandler = ImageHandler('Images/arrow.jpg',pygame.Vector2(), game)
        self.position = originObject.imageHandler.getCenter() - self.imageHandler.getCenter()
        self.imageHandler.position = self.position
        self.targetPosition = targetCenter - self.imageHandler.getCenter()
        self.transformhandler = TransformHandler(self.game, self.position)
        self.transformhandler.direction = (targetCenter- self.position)
        self.transformhandler.speed = .03
        self.imageHandler.setAngle(math.degrees(math.atan2(self.transformhandler.direction.x, self.transformhandler.direction.y)) + 180)
        self.targetRect = self.targetImageHandler.getRect()
        self.originObject = originObject
        self.targetObject = targetObject

    def update(self):
        arrowRect = self.imageHandler.getRect()

        if(arrowRect.colliderect(self.targetRect)):
            self.originObject.dealDamage(self.targetObject)
            self.delete()

    def delete(self):
        self.game.arrowFlies = 0
        self.game.gameObjects.remove(self)
        self.game.gameObjects.remove(self.transformhandler)
        self.game.gameObjects.remove(self.imageHandler)