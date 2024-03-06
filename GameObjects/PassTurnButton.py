from asyncio.windows_events import NULL
from GameObjects.GameObject import GameObject
import pygame
from Handlers.ImageHandler import ImageHandler
from Handlers.ClickHandler import ClickHandler

class PassTurnButton(GameObject):
    def __init__(self,game):
        super().__init__(game)
        self.handlers = []
        self.position = pygame.Vector2(game.SCREEN_WIDTH - 200, game.SCREEN_HEIGHT/2 - 50)
        self.rect = pygame.Rect(self.position.x,self.position.y,100,100)
        self.imageHandler = ImageHandler('images/PassTurn.png',self.position, game)
        self.clicker = ClickHandler(self.rect, self.onClick, (game), game)
        self.turnRectangleY = [0, 450]

    def onClick(self, game):
        game.currentState['selectedCard'] = NULL
        for player in game.currentState['players']:
            for card in player.field:
                card.attackUsed = 0
        
        game.currentState['turn'] = int(game.currentState['turn'] == 0)
        
        game.currentState['players'][game.currentState['turn']].totalMana += 1
        game.currentState['players'][game.currentState['turn']].setMana(game.currentState['players'][game.currentState['turn']].totalMana)

        if len(game.currentState['players'][game.currentState['turn']].hand) < 5 and len(game.currentState['players'][game.currentState['turn']].deck) > 0:
            game.currentState['players'][game.currentState['turn']].drawCard()
        game.currentState['turnRectangle'].y = self.turnRectangleY[game.currentState['turn']]



