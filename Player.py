import pygame
from Card import Card
from GameObject import GameObject
from Handlers.TextHandler import TextHandler
import random

class Player(GameObject):
    def __init__(self, game, num) -> None:
        super().__init__(game)
        self.health = [20]
        self.totalMana = int(num == 0)
        self.mana = int(num == 0)
        self.deck = []
        self.hand = []
        self.field = []
        self.num = num
        self.game = game
        UIBaseManaX = game.SCREEN_WIDTH - 200
        UIBaseManaY = [50, game.SCREEN_HEIGHT-100]
        self.healthText = TextHandler(game, 'Health: ' + str(self.health[0]), 1, pygame.Vector2(0,0), pygame.Vector2(UIBaseManaX, UIBaseManaY[self.num]))
        self.manaText = TextHandler(game, 'Mana: ' + str(self.mana) + '/' + str(self.totalMana), 1,pygame.Vector2(0,0), pygame.Vector2(UIBaseManaX, UIBaseManaY[self.num] + game.font.size('1')[1]))
        self.handY = handY = [0, self.game.SCREEN_HEIGHT - 205]

        for x in range(10):
            self.deck.append(Card('TGuy1', 1, 1, 1, num, game))
        for x in range(10):
            self.deck.append(Card('TGuy2', 2, 2, 2, num, game))
        for x in range(10):
            self.deck.append(Card('TGuy3', 3, 3, 3, num, game))

        random.shuffle(self.deck)

        handPositionY = [5, game.SCREEN_HEIGHT - 205]

        for x in range(5):
            self.deck[-1].position.x = cardPositionX(num)
            self.deck[-1].position.y = handPositionY[num]
            self.hand.append(self.deck[-1])
            self.deck.pop(-1)

    def update(self):
        self.healthText.str = 'Health: ' + str(self.health[0])
        self.manaText.str = 'Mana: ' + str(self.mana) + '/' + str(self.totalMana)
        for index, card in enumerate(self.hand):
            card.position.x = 5 + 205 * (index + 1)
            card.position.y = self.handY[self.num]

def cardPositionX(i):
    return 5 + 205 * (i + 1)