import Colors
from Colors import *
import pygame

from GameObjects.GameObject import GameObject
from Handlers.ImageHandler import ImageHandler

# class TextHandler(GameObject):
#     def __init__(self, game, str, basePosition, positionOffset, font) -> None:
#         super().__init__(game)
#         self.str = str
#         self.game = game
#         self.basePosition = basePosition
#         self.positionOffset = positionOffset
#         self.position = self.basePosition + self.positionOffset
#         self.color = WHITE
#         self.font = font
#         self.imageHandler = ImageHandler('Images/bird.jpg',self.position,self.game)
#         self.imageHandler.image = self.font.render(self.str, 1, self.color)
    
#     def update(self):
#         self.position = self.basePosition + self.positionOffset
#         self.img = self.font.render(self.str, 1, self.color)
#         self.draw()

#     def draw(self):
#         self.drawOutlineText(self.game, self.str)

#     def drawOutlineText(self, game, str):
#         outlineSize = 1
#         outlineImg = self.font.render(str, 1, BLACK)
#         game.screen.blit(outlineImg, (self.position.x + outlineSize, self.position.y + outlineSize))
#         game.screen.blit(outlineImg, (self.position.x - outlineSize, self.position.y + outlineSize))
#         game.screen.blit(outlineImg, (self.position.x + outlineSize, self.position.y - outlineSize))
#         game.screen.blit(outlineImg, (self.position.x - outlineSize, self.position.y - outlineSize))
#         game.screen.blit(self.img, self.position)

#     def getRect(self):
#         rect = self.img.get_rect()
#         rect.x = self.position.x
#         rect.y = self.position.y
#         return rect

#     def getCenter(self):
#         return pygame.Vector2(self.position.x + self.img.get_rect().width/2, self.position.y + self.img.get_rect().height/2)

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

        self.imageHandlers = []
        for i in range(4):
            self.imageHandlers.append(ImageHandler('Images/bird.jpg',self.position,self.game))

        outlineSize = 1
        self.imageHandlers[0].position = (self.position.x + outlineSize, self.position.y + outlineSize)
        self.imageHandlers[1].position = (self.position.x - outlineSize, self.position.y + outlineSize)
        self.imageHandlers[2].position = (self.position.x + outlineSize, self.position.y - outlineSize)
        self.imageHandlers[3].position = (self.position.x - outlineSize, self.position.y - outlineSize)

        self.imageHandler = ImageHandler('Images/bird.jpg',self.position,self.game)
        # self.imageHandler.position = self.position
        
    def update(self):
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

        # self.draw()

    # def draw(self):
    #     self.drawOutlineText(self.game, self.str)

    # def drawOutlineText(self, game, str):
    #     outlineSize = 1
    #     outlineImg = self.font.render(str, 1, BLACK)
    #     game.screen.blit(outlineImg, (self.position.x + outlineSize, self.position.y + outlineSize))
    #     game.screen.blit(outlineImg, (self.position.x - outlineSize, self.position.y + outlineSize))
    #     game.screen.blit(outlineImg, (self.position.x + outlineSize, self.position.y - outlineSize))
    #     game.screen.blit(outlineImg, (self.position.x - outlineSize, self.position.y - outlineSize))
    #     game.screen.blit(self.img, self.position)

    # def getRect(self):
    #     rect = self.img.get_rect()
    #     rect.x = self.position.x
    #     rect.y = self.position.y
    #     return rect

    # def getCenter(self):
    #     return pygame.Vector2(self.position.x + self.img.get_rect().width/2, self.position.y + self.img.get_rect().height/2)