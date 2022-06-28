import Colors
import pygame

class TextHandler:
    def __init__(self, game, str, relativeX, relativeY, isOutline, object) -> None:
        self.str = str
        self.isOutline = isOutline
        self.game = game
        self.relativeX = relativeX
        self.relativeY = relativeY
        self.position = pygame.Vector2()
        self.object = object
        self.object.handlers.append(self)
    
    def update(self):
        self.position.x = self.object.position.x + self.relativeX
        self.position.y = self.object.position.y + self.relativeY
        self.draw()

    def draw(self):
        if(self.isOutline):
            self.drawOutlineText(self.game, self.str, self.position.x, self.position.y)
        else:
            self.game.screen.blit(self.game.font.render(self.str, Colors.BLACK), (self.position.x, self.position.y))

    def drawOutlineText(self, game,str,x,y):
        game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x + 1, y + 1))
        game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x - 1, y + 1))
        game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x + 1, y - 1))
        game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x - 1, y - 1))
        game.screen.blit(game.font.render(str, 1, Colors.WHITE), (x, y))
