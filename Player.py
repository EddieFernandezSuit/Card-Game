import pygame
from GameObject import GameObject
from Handlers.TextHandler import TextHandler


class Player(GameObject):
    def __init__(self, game, num) -> None:
        super().__init__(game)
        self.health = 20
        self.totalMana = int(num == 0)
        self.mana = 1
        self.deck = []
        self.hand = []
        self.field = []
        self.num = num
        self.game = game
        UIBaseManaX = game.SCREEN_WIDTH - 200
        UIBaseManaY = [50, game.SCREEN_HEIGHT-100]
        self.healthText = TextHandler(game, 'Health: ' + str(self.health), 1, pygame.Vector2(0,0), pygame.Vector2(UIBaseManaX, UIBaseManaY[self.num]))
        self.manaText = TextHandler(game, 'Mana: ' + str(self.mana) + '/' + str(self.totalMana), 1,pygame.Vector2(0,0), pygame.Vector2(UIBaseManaX, UIBaseManaY[self.num] + game.font.size('1')[1]))

    def update(self):
        self.healthText.str = 'Health: ' + str(self.health)
        self.manaText = 'Mana: ' + str(self.mana)
        handY = [0, self.game.SCREEN_HEIGHT - 205]
        for index, card in enumerate(self.hand):
            card.position.x = 5 + 205 * (index + 1)
            card.position.y = handY[self.num]