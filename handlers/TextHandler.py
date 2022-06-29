import Colors
import pygame

from GameObject import GameObject

class TextHandler(GameObject):
    def __init__(self, game, str, isOutline, position, positionOffset) -> None:
        super().__init__(game)
        self.str = str
        self.isOutline = isOutline
        self.game = game
        self.basePosition = position
        self.positionOffset = positionOffset
        # self.truePosition = position + positionOffset
    
    def update(self):
        # self.truePosition = self.basePosition + self.positionOffset
        self.draw()

    def draw(self):
        if(self.isOutline):
            self.drawOutlineText(self.game, self.str, self.basePosition + self.positionOffset)
        else:
            self.game.screen.blit(self.game.font.render(self.str, Colors.BLACK), (self.truePosition))

    def drawOutlineText(self, game, str, position):
        x = position.x
        y = position.y
        game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x + 1, y + 1))
        game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x - 1, y + 1))
        game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x + 1, y - 1))
        game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x - 1, y - 1))
        game.screen.blit(game.font.render(str, 1, Colors.WHITE), (x, y))
