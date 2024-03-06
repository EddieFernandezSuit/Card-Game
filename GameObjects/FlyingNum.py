import pygame
from GameObjects.GameObject import GameObject
from Handlers.TextHandler import TextHandler
from Handlers.TransformHandler import TransformHandler
from Timer import Timer

class FlyingNum(GameObject):
    def __init__(self, game, str, position, color) -> None:
        super().__init__(game)
        pos = pygame.Vector2(position.x, position.y)
        self.textHandler = TextHandler(game, str, pos, pygame.Vector2(0,100), self.game.fonts["small"])
        self.textHandler.color = color
        self.transform = TransformHandler(game, pos)
        self.transform.speed = 2
        self.transform.gravity = .03
        self.transform.direction = (position - pygame.Vector2(position.x, position.y + 1)).normalize()
        self.timer = Timer(60, self.destroy)

    def update(self):
        self.timer.update()

    def destroy(self):
        self.textHandler.delete()
        self.game.currentState['gameObjects'].remove(self.transform)
        self.game.currentState['gameObjects'].remove(self)
        del self
