from requests import delete
import Colors
from Colors import *
import pygame

from GameObjects.GameObject import GameObject
from Handlers.ImageHandler import ImageHandler

class TextHandler(GameObject):
    def __init__(self, game, str, basePosition, positionOffset, font) -> None:
        super().__init__(game)
        self.str = str
        self.game = game
        self.basePosition = basePosition
        self.positionOffset = positionOffset
        self.position = self.basePosition + self.positionOffset
        self.color = WHITE
        self.font = font
        self.width, self.height = self.font.size(self.str)
        self.rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)

        self.imageHandlers = []
        for i in range(4):
            self.imageHandlers.append(ImageHandler('Images/bird.jpg',self.position,self.game))

        outlineSize = 1
        self.imageHandlers[0].position = (self.position.x + outlineSize, self.position.y + outlineSize)
        self.imageHandlers[1].position = (self.position.x - outlineSize, self.position.y + outlineSize)
        self.imageHandlers[2].position = (self.position.x + outlineSize, self.position.y - outlineSize)
        self.imageHandlers[3].position = (self.position.x - outlineSize, self.position.y - outlineSize)

        self.imageHandler = ImageHandler('Images/bird.jpg',self.position,self.game)
        
    def update(self):
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        self.position = self.basePosition + self.positionOffset
        self.imageHandler.image = self.font.render(self.str, 1, self.color)
        self.imageHandler.position = self.position

        for i in range(4):
            self.imageHandlers[i].image = self.font.render(self.str,1, Colors.BLACK)
            outlineSize = 1
            self.imageHandlers[0].position = (self.position.x + outlineSize, self.position.y + outlineSize)
            self.imageHandlers[1].position = (self.position.x - outlineSize, self.position.y + outlineSize)
            self.imageHandlers[2].position = (self.position.x + outlineSize, self.position.y - outlineSize)
            self.imageHandlers[3].position = (self.position.x - outlineSize, self.position.y - outlineSize)

    def delete(self):
        for imageHandler in self.imageHandlers:
            self.game.currentState['gameObjects'].remove(imageHandler)
        self.game.currentState['gameObjects'].remove(self.imageHandler)
        self.game.currentState['gameObjects'].remove(self)