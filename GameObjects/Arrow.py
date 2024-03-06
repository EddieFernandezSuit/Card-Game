import math
import random
import pygame
from GameObjects.GameObject import GameObject
from Handlers.ImageHandler import ImageHandler
from Handlers.TransformHandler import TransformHandler

class Arrow(GameObject):
    def __init__(self, game, originObject, targetObject) -> None:
        super().__init__(game)
        targetCenter = 0
        self.used = 0
        self.targetImageHandler = 0
        if (type(originObject) != type(targetObject)):
            self.targetImageHandler = targetObject.healthText.imageHandler
        else:
            self.targetImageHandler = targetObject.imageHandler
        targetCenter = self.targetImageHandler.getCenter()
        self.imageHandler = ImageHandler('Images/arrow.jpg', pygame.Vector2(), game)
        self.position = originObject.imageHandler.getCenter() - self.imageHandler.getCenter()
        self.position.x += random.randint(-50,50)
        self.imageHandler.position = self.position
        self.targetPosition = targetCenter - self.imageHandler.getCenter()
        self.transformhandler = TransformHandler(self.game, self.position)
        self.transformhandler.direction = (targetCenter - self.position).normalize()
        self.transformhandler.speed = 50
        self.imageHandler.setAngle(math.degrees(math.atan2(self.transformhandler.direction.x, self.transformhandler.direction.y)) + 180)
        self.targetRect = self.targetImageHandler.getRect()
        self.originObject = originObject
        self.targetObject = targetObject

    def update(self):
        arrowRect = self.imageHandler.getRect()
        if(arrowRect.colliderect(self.targetRect)):
            if self.used == 0:
                self.targetObject.impaledArrows.append(self)
                self.originObject.dealDamage(self.targetObject)
                self.used = 1
                self.transformhandler.speed = 0
                self.game.currentState['arrowFlies'] = 0
                # self.delete()

    def delete(self):
        self.game.currentState["arrowFlies"] = 0
        self.game.currentState['gameObjects'].remove(self)
        self.game.currentState["gameObjects"].remove(self.transformhandler)
        self.game.currentState['gameObjects'].remove(self.imageHandler)