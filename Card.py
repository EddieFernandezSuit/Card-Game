
from asyncio.windows_events import NULL
import pygame
from GameObject import GameObject
from handlers.ImageHandler import ImageHandler
from handlers.Clicker import Clicker
import Colors
from handlers.TextHandler import TextHandler
from GameObject import GameObject

class Card(GameObject):
    x = 0
    y = 0
    def __init__(self, name, mana, damage, health, playerNum, game) -> None:
        super().__init__(game)
        self.name = name
        self.mana = mana
        self.damage = damage
        self.health = health
        self.image = pygame.image.load('images/jungle.jpg')
        self.rect = self.image.get_rect()
        self.playerNum = playerNum
        self.place = 'hand'
        self.fieldPosition = 0
        self.attackUsed = 0
        self.clicker = Clicker(self.rect, self.onClick, (game), self)
        self.imageHandler = ImageHandler(self.image, self, game.screen)
        self.statsStr = [str(self.name), 'M: ' + str(self.mana), 'D: ' + str(self.damage), 'H: ' + str(self.health)]
        self.statsText = []
        for index, statStr in enumerate(self.statsStr):
            self.statsText.append(TextHandler(game, statStr ,5, 5 + game.font.size(statStr)[1] * index, 1, self))

    def onClick(self, game):
        if game.selectedCard == self:
            game.selectedCard = NULL
        elif game.selectedCard == NULL:
            if len(game.players[int(self.playerNum == 0)].field) == 0 and self.place == 'field' and self.attackUsed == 0:
                self.attackUsed = 1
                game.players[int(self.playerNum == 0)].health -= self.damage
            elif game.turn == self.playerNum and ((self.place == 'hand' and game.players[self.playerNum].mana >= self.mana and game.turn == self.playerNum) or (self.place == 'field' and self.attackUsed == 0)):
                game.selectedCard = self
        else:
            if self.place == 'field' and game.selectedCard.place == 'field':
                self.damage(game.selectedCard, self, game)
                game.selectedCard.attackUsed = 1
                game.selectedCard = NULL

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.clicker.update()
        self.imageHandler.update()
        for text in self.statsText:
            text.update()
        # self.draw(game)

    # def draw(self, game):
    #     temp = [str(self.name), 'M: ' + str(self.mana), 'D: ' + str(self.damage), 'H: ' + str(self.health)]
    #     for y in range(len(temp)):
    #         drawOutlineText(game, temp[y] ,self.x + 5, self.y + 5 + y * game.font.size(temp[y])[1])

    def damage(damager,damaged,game):
        damaged.health -= damager.damage
        if damaged.health <= 0:
            game.players[damaged.playerNum].field.remove(damaged)
            game.cards.remove(damaged)

