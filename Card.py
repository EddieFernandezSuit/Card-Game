
from asyncio.windows_events import NULL
from turtle import position
import pygame
from GameObject import GameObject
from Handlers.ImageHandler import ImageHandler
from Handlers.Clicker import Clicker
from Handlers.TextHandler import TextHandler
from GameObject import GameObject
from Arrow import Arrow

class Card(GameObject):
    def __init__(self, name, mana, damage, health, playerNum, game) -> None:
        super().__init__(game)
        self.game = game
        self.position = pygame.Vector2(-200,0)
        self.name = name
        self.mana = mana
        self.damage = damage
        self.health = health
        self.playerNum = playerNum
        self.place = 'hand'
        self.fieldPosition = 0
        self.attackUsed = 0
        self.imageHandler = ImageHandler('images/jungle.jpg', self.position, game)
        self.rect = self.imageHandler.image.get_rect()
        self.clicker = Clicker(self.rect, self.onClick, (game), game)
        self.statsStr = [str(self.name), 'M: ' + str(self.mana), 'D: ' + str(self.damage), 'H: ' + str(self.health)]
        self.statsText = []
        for index, statStr in enumerate(self.statsStr):
            self.statsText.append(TextHandler(game, statStr, 1, self.position, pygame.Vector2(5,5 + game.font.size(statStr)[1] * index)))

    def onClick(self, game):
        if game.selectedCard == self:
            game.selectedCard = NULL
        elif game.selectedCard == NULL:
            if len(game.players[int(self.playerNum == 0)].field) == 0 and self.place == 'field' and self.attackUsed == 0:
                self.attackUsed = 1
                game.players[int(self.playerNum == 0)].health -= self.damage
                rect = game.players[int(self.playerNum == 0)].healthText.img.get_rect()
                rect.x += game.players[int(self.playerNum == 0)].healthText.truePosition.x
                rect.y += game.players[int(self.playerNum == 0)].healthText.truePosition.y
                Arrow(game, self.imageHandler.getCenter(), game.players[int(self.playerNum == 0)].healthText.truePosition, rect)
            elif game.turn == self.playerNum and ((self.place == 'hand' and game.players[self.playerNum].mana >= self.mana and game.turn == self.playerNum) or (self.place == 'field' and self.attackUsed == 0)):
                game.selectedCard = self
        elif self.place == 'field' and game.selectedCard.place == 'field':
            selectedCardRect = game.selectedCard.imageHandler.image.get_rect()
            selectedCardRect.x += game.selectedCard.position.x
            selectedCardRect.y += game.selectedCard.position.y
            Arrow(game, game.selectedCard.imageHandler.getCenter(), self.imageHandler.getCenter(), selectedCardRect)
            # self.dealDamage(game.selectedCard, self, game)
            # game.selectedCard.attackUsed = 1
            # game.selectedCard = NULL
    
    

    def delete(self):
        for statsText in self.statsText:
            self.game.gameObjects.remove(statsText)
        self.game.gameObjects.remove(self.clicker)
        self.game.gameObjects.remove(self.imageHandler)

        self.game.players[self.playerNum].field.remove(self)
        self.game.cards.remove(self)
        self.game.gameObjects.remove(self)

    def update(self):
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def dealDamage(self, damager, damaged, game):
        damaged.health -= damager.damage
        self.statsText[3].str = 'H: ' + str(self.health)
        if damaged.health <= 0:
            self.delete()

