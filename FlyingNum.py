import pygame
import random
from GameObject import GameObject
from Handlers.TextHandler import TextHandler
from Handlers.TransformHandler import TransformHandler
from Timer import Timer

class FlyingNum(GameObject):
    def __init__(self, game, str, position) -> None:
        super().__init__(game)
        self.textHandler = TextHandler(game, str, 0, position, pygame.Vector2(100,100))
        self.transform = TransformHandler(game, position)
        self.transform.speed = 3
        self.transform.gravity = .1
        self.transform.direction = (position - pygame.Vector2(position.x, position.y + 1)).normalize()
        self.timer = Timer(50, self.destroy)

    def update(self):
        self.timer.update()

    def destroy(self):
        self.game.gameObjects.remove(self.textHandler)
        self.game.gameObjects.remove(self.transform)
        self.game.gameObjects.remove(self)
        del self
