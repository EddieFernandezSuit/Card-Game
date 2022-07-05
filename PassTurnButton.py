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
        game.selectedCard = NULL
        for player in game.players:
            for card in player.field:
                card.attackUsed = 0
        
        game.turn = int(game.turn == 0)
        game.players[game.turn].totalMana += 1
        game.players[game.turn].mana = game.players[0].totalMana
        turnRectangleY = [0, 450]
        game.turnRectangle.y = turnRectangleY[game.turn]



