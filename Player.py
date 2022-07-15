import pygame
from Card import Card
from Game import Game
from Zone import Zone
from GameObject import GameObject
from Handlers.TextHandler import TextHandler
import random

class Player(GameObject):
    def __init__(self, game, num) -> None:
        super().__init__(game)
        self.stats = {
            'Armor': 0,
            'Health': 20
        }
        # self.health = [20]
        self.armor = 0
        self.totalMana = int(num == 0)
        self.mana = int(num == 0)
        self.deck = []
        self.hand = []
        self.field = []
        self.zones = []
        self.num = num
        self.game = game
        UIBaseManaX = game.SCREEN_WIDTH - 200
        UIBaseManaY = [50, game.SCREEN_HEIGHT-100]
        self.healthText = TextHandler(game, 'Health: ' + str(self.stats['Health']), 1, pygame.Vector2(0,0), pygame.Vector2(UIBaseManaX, UIBaseManaY[self.num]))
        self.manaText = TextHandler(game, 'Mana: ' + str(self.mana) + '/' + str(self.totalMana), 1,pygame.Vector2(0,0), pygame.Vector2(UIBaseManaX, UIBaseManaY[self.num] + game.font.size('1')[1]))
        
        self.handY = [5, self.game.SCREEN_HEIGHT - 205]
        fieldPositionY = [210, game.SCREEN_HEIGHT - 410]

        for y in range(5):
            self.zones.append(Zone(pygame.Vector2(cardPositionX(y), fieldPositionY[num]), num, game))

        def addCard(cardName):
            self.deck.append(Card(self.game, self.num, cardName))

        for x in range(3):
            addCard('Jungle Delver')
            addCard('Bird')
            addCard('Turtle')
            addCard('Armordillo')
            # addCard('Bats')
            
        random.shuffle(self.deck)

        for x in range(4):
            self.drawCard()

    
    def drawCard(self):
        handPositionY = [5, self.game.SCREEN_HEIGHT - 205]
        self.hand.append(self.deck[-1])
        self.deck.pop(-1)
        self.hand[-1].position.x = cardPositionX(len(self.hand)-1)
        self.hand[-1].position.y = handPositionY[self.num]
        
    def update(self):
        self.healthText.str = 'Health: ' + str(self.stats['Health'])
        self.manaText.str = 'Mana: ' + str(self.mana) + '/' + str(self.totalMana)
        for index, card in enumerate(self.hand):
            card.position.x = cardPositionX(index)
            card.position.y = self.handY[self.num]

    def delete(self):
        for player in self.game.players:
            if player.stats['Health'] <= 0:
                print('Player ' + str(player.num + 1) + ' wins')
                self.game = Game(self.game.start,self.game.update,self.game.draw)

    def setHealth(self, health):
        self.stats['Health'] = health   

def cardPositionX(i):
    return 5 + 210 * (i + 1)