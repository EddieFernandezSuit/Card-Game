from asyncio.windows_events import NULL
from Handlers.ImageHandler import ImageHandler
from Handlers.TextHandler import TextHandler
from Handlers.Clicker import Clicker
from GameObject import GameObject
from FlyingNum import FlyingNum
from Arrow import Arrow
import pygame
import Colors

class Card(GameObject):
    def __init__(self, name, mana, damage, health, playerNum, game, growthType, splash) -> None:
        super().__init__(game)
        self.game = game
        self.position = pygame.Vector2(-200,0)
        self.name = name
        self.mana = mana
        self.damage = damage
        self.health = [health]
        self.splash = splash
        self.growthType = growthType
        self.growthStat = self.health
        self.playerNum = playerNum
        self.place = 'hand'
        self.fieldPosition = 0
        self.attackUsed = 0
        self.imageHandler = ImageHandler('images/jungle.jpg', self.position, game)
        self.rect = self.imageHandler.image.get_rect()
        self.clicker = Clicker(self.rect, self.onClick, (), game)
        self.statsStr = [self.name, 'M ' + str(self.mana), 'D ' + str(self.damage), 'H ' + str(self.health[0])]
        self.statsText = []
        if splash > 0:
            self.statsStr.append('Splash '+str(self.splash))
        self.emptyZone = 0
        for index, statStr in enumerate(self.statsStr):
            self.statsText.append(TextHandler(game, statStr, 1, self.position, pygame.Vector2(5,5 + game.font.size(statStr)[1] * index)))
        
        growthStats ={
            'damage': 2,
            'health': 3,
            'splash': 4
        }
        self.statsText[growthStats[growthType]].color = Colors.LIGHTCYAN

    def onClick(self, none):
        if self.game.selectedCard == self:
            self.game.selectedCard = NULL
        elif self.game.selectedCard == NULL:
            if self.place == 'field' and self.attackUsed == 0:
                if len(self.game.players[int(self.playerNum == 0)].field) == 0:
                    self.attackUsed = 1
                    Arrow(self.game, self.imageHandler.getCenter(), self.game.players[int(self.playerNum == 0)].healthText.position, self.game.players[int(self.playerNum == 0)].healthText.getRect(), self, self.game.players[int(self.playerNum == 0)])
                elif self.splash > 0:
                    count = 0
                    for card in self.game.players[int(self.playerNum == 0)].field:
                        if count <= self.splash:
                            Arrow(self.game, self.imageHandler.getCenter(), card.imageHandler.getCenter(), card.imageHandler.getRect(), self, card)
                            count += 1 
                else:
                    self.game.selectedCard = self
            elif self.place == 'hand' and self.game.players[self.playerNum].mana >= self.mana and self.game.turn == self.playerNum:
                self.game.selectedCard = self
                for zone in self.game.players[self.playerNum].zones:
                    if zone.isFull == 0:
                        zone.click(self.game)
                        break
            
        elif self.place == 'field' and self.game.selectedCard.place == 'field':
            Arrow(self.game, self.game.selectedCard.imageHandler.getCenter(), self.imageHandler.getCenter(), self.imageHandler.getRect(), self.game.selectedCard, self)
            self.game.selectedCard.attackUsed = 1
            self.game.selectedCard = NULL

    def delete(self):
        for statsText in self.statsText:
            self.game.gameObjects.remove(statsText)
        
        self.emptyZone.isFull = 0
        self.game.gameObjects.remove(self.clicker)
        self.game.gameObjects.remove(self.imageHandler)
        self.game.players[self.playerNum].field.remove(self)
        self.game.gameObjects.remove(self)

    def update(self):
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        self.statsText[3].str = 'H ' + str(self.health[0])

    def dealDamage(self, target):
        target.health[0] -= self.damage
        if type(target) == type(self):
            FlyingNum(self.game, '- ' + str(self.damage) + ' health', target.position, Colors.RED)
        if target.health[0] <= 0:
            target.delete()
            if self.growthType == 'health':
                self.growthStat[0] += 1
            elif self.growthType == 'damage':
                self.damage += 1
                self.statsText[2].str = 'D ' + str(self.damage)
            FlyingNum(self.game, '+ 1 ' + str(self.growthType), self.position, Colors.GREEN)
            
