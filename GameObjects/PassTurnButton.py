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
        for player in game.states[game.currentState]['players']:
            for card in player.field:
                card.attackUsed = 0
        
        game.states[game.currentState]['turn'] = int(game.states[game.currentState]['turn'] == 0)
        
        game.states[game.currentState]['players'][game.states[game.currentState]['turn']].totalMana += 1
        game.states[game.currentState]['players'][game.states[game.currentState]['turn']].setMana(game.states[game.currentState]['players'][game.states[game.currentState]['turn']].totalMana)

        if len(game.states[game.currentState]['players'][game.states[game.currentState]['turn']].hand) < 5 and len(game.states[game.currentState]['players'][game.states[game.currentState]['turn']].deck) > 0:
            game.states[game.currentState]['players'][game.states[game.currentState]['turn']].drawCard()
        game.states[game.currentState]['turnRectangle'].y = self.turnRectangleY[game.states[game.currentState]['turn']]



