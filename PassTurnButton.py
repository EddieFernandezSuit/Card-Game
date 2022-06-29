from asyncio.windows_events import NULL
from GameObject import GameObject
import pygame
from Handlers.ImageHandler import ImageHandler
from Handlers.Clicker import Clicker

class PassTurnButton(GameObject):
    def __init__(self,game):
        super().__init__(game)
        self.handlers = []
        self.position = pygame.Vector2(game.SCREEN_WIDTH - 200, game.SCREEN_HEIGHT/2 - 25)
        self.rect = pygame.Rect(self.position.x,self.position.y,50,50)
        self.imageHandler = ImageHandler('images/PassTurn.png',self.position, game)
        self.clicker = Clicker(self.rect, self.onClick, (game), game)

    def onClick(self, game):
        for i in range(len(game.cards)):
            game.selectedCard = NULL
            game.cards[i].attackUsed = 0
        if game.phase == 'play':
            for j in range(len(game.emptyZones)):
                game.emptyZones[j].isFull = 0
                for i in range(len(game.cards)):
                    if game.cards[i].position.x == game.emptyZones[j].position.x and game.cards[i].position.y == game.emptyZones[j].position.y:
                        game.emptyZones[j].isFull = 1
            game.phase = 'play'
            game.turn = int(game.turn == 0)
            game.players[game.turn].totalMana += 1
            game.players[game.turn].mana = game.players[0].totalMana
            turnRectangleY = [0, 450]
            game.turnRectangle.y = turnRectangleY[game.turn]



