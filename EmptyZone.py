from asyncio.windows_events import NULL
from GameObject import GameObject
from Handlers.ImageHandler import ImageHandler
import pygame
from Handlers.Clicker import Clicker

class EmptyZone(GameObject):
    def __init__(self, position, playerNum, game):
        super().__init__(game)
        self.imageHandler = ImageHandler(pygame.image.load('images/emptyZone.png'),self,game.screen)
        self.position = position
        self.rect = pygame.Rect(self.position.x,self.position.y,200,200)
        self.isFull = 0
        self.playerNum = playerNum
        self.clicker = Clicker(self.rect, self.click, (game), self)
    
    def click(self, game):
        if self.isFull == 0 and game.selectedCard != NULL and self.playerNum == game.selectedCard.playerNum and game.selectedCard.place == 'hand':
            game.selectedCard.place = 'field'
            game.players[self.playerNum].field.append(game.selectedCard)
            game.selectedCard.position.x = self.position.x
            game.selectedCard.position.y = self.position.y
            self.isFull = 1
            game.players[game.selectedCard.playerNum].mana -= game.selectedCard.mana
            for k in range(len(game.players[game.selectedCard.playerNum].hand)):
                if game.players[game.selectedCard.playerNum].hand[k] == game.selectedCard:
                    game.players[game.selectedCard.playerNum].hand.pop(k)
                    break
            game.selectedCard = NULL
