from asyncio.windows_events import NULL
from GameObjects.GameObject import GameObject
from Handlers.ImageHandler import ImageHandler
import pygame
from Handlers.ClickHandler import Clicker

class Zone(GameObject):
    def __init__(self, position, playerNum, game):
        super().__init__(game)
        self.position = position
        self.rect = pygame.Rect(self.position.x,self.position.y,200,200)
        self.isFull = 0
        self.playerNum = playerNum
        self.clicker = Clicker(self.rect, self.click, (game), game)
        self.game = game
    
    def click(self, game):
        if self.isFull == 0 and self.game.states[self.game.currentState]['selectedCard'] != NULL and self.playerNum == self.game.states[self.game.currentState]['selectedCard'].playerNum and self.game.states[self.game.currentState]['selectedCard'].place == 'hand':
            self.game.states[self.game.currentState]['selectedCard'].place = 'field'
            self.game.states[self.game.currentState]['players'][self.game.states[self.game.currentState]['selectedCard'].playerNum].field.append(self.game.states[self.game.currentState]['selectedCard'])
            self.game.states[self.game.currentState]['selectedCard'].position.x = self.position.x
            self.game.states[self.game.currentState]['selectedCard'].position.y = self.position.y
            self.isFull = 1
            self.game.states[self.game.currentState]['players'][self.game.states[self.game.currentState]['selectedCard'].playerNum].mana -= self.game.states[self.game.currentState]['selectedCard'].stats['Mana']
            for k in range(len(self.game.states[self.game.currentState]['players'][self.game.states[self.game.currentState]['selectedCard'].playerNum].hand)):
                if self.game.states[self.game.currentState]['players'][self.game.states[self.game.currentState]['selectedCard'].playerNum].hand[k] == self.game.states[self.game.currentState]['selectedCard']:
                    self.game.states[self.game.currentState]['players'][self.game.states[self.game.currentState]['selectedCard'].playerNum].hand.pop(k)
                    break
            self.game.states[self.game.currentState]['selectedCard'].emptyZone = self
            self.game.states[self.game.currentState]['selectedCard'] = NULL