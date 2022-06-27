import Colors


class TextHandler:
    def __init__(self, game, str, relativeX, relativeY, isOutline, object) -> None:
        self.str = str
        self.isOutline = isOutline
        self.game = game
        self.relativeX = relativeX
        self.relativeY = relativeY
        self.x = 0 
        self.y = 0
        self.object = object
    
    def update(self):
        self.x = self.object.x + self.relativeX
        self.y = self.object.y + self.relativeY
        self.draw()

    def draw(self):
        if(self.isOutline):
            self.drawOutlineText(self.game, self.str, self.x, self.y)
        else:
            self.game.screen.blit(self.game.font.render(self.str, Colors.BLACK), (self.x, self.y))

    def drawOutlineText(self, game,str,x,y):
        game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x + 1, y + 1))
        game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x - 1, y + 1))
        game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x + 1, y - 1))
        game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x - 1, y - 1))
        game.screen.blit(game.font.render(str, 1, Colors.WHITE), (x, y))
