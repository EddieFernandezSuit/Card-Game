from asyncio.windows_events import NULL
from GameObjects.GameObject import GameObject
import pygame
from Handlers.ImageHandler import ImageHandler
from Handlers.ClickHandler import Clicker

class PassTurnButton(GameObject):
    def __init__(self,game):
        super().__init__(game)
        self.handlers = []
        self.position = pygame.Vector2(game.SCREEN_WIDTH - 200, game.SCREEN_HEIGHT/2 - 50)
        self.rect = pygame.Rect(self.position.x,self.position.y,100,100)
        self.imageHandler = ImageHandler('images/PassTurn.png',self.position, game)
        self.clicker = Clicker(self.rect, self.onClick, (game), game)
        self.turnRectangleY = [0, 450]

    def onClick(self, game):
        game.selectedCard = NULL
        for player in game.players:
            for card in player.field:
                card.attackUsed = 0
        
        game.turn = int(game.turn == 0)
        
        game.players[game.turn].totalMana += 1
        game.players[game.turn].setMana(game.players[game.turn].totalMana)

        if len(game.players[game.turn].hand) < 5 and len(game.players[game.turn].deck) > 0:
            game.players[game.turn].drawCard()
        game.turnRectangle.y = self.turnRectangleY[game.turn]



