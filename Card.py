from asyncio.windows_events import NULL
from Game import Game
from Handlers.ImageHandler import ImageHandler
from Handlers.TextHandler import TextHandler
from Handlers.Clicker import Clicker
from GameObject import GameObject
from FlyingNum import FlyingNum
from Arrow import Arrow
import pygame
import Colors
import json
from Particle import Particle

class Card(GameObject):
    def __init__(self, game, playerNum, name) -> None:
        super().__init__(game)

        cardData = json.load(open('cardData.json'))
        self.stats = cardData[name]
        self.name = name
        self.game = game
        self.position = pygame.Vector2(-200,0)
        self.playerNum = playerNum
        self.place = 'hand'
        self.attackUsed = 0
        self.imageHandler = ImageHandler('images/' + self.name.lower() + '.jpg', self.position, game)
        self.rect = self.imageHandler.image.get_rect()
        self.clicker = Clicker(self.rect, self.onClick, (), game)
        self.statsText = {}
        self.emptyZone = 0
        ncount = 0
        self.statsText['Name'] = TextHandler(game, self.name, 1, self.position, pygame.Vector2(5,5 + game.smallFont.size('A')[1] * ncount), self.game.smallFont)
        for key in self.stats:
            if self.stats[key] != 0 and key != 'Growth Type':
                ncount += 1
                self.statsText[key] = TextHandler(game, key + ' ' +  str(self.stats[key]), 1, self.position, pygame.Vector2(5,5 + game.smallFont.size('A')[1] * ncount), self.game.smallFont)

        self.statsText[self.stats['Growth Type']].color = Colors.LIGHTCYAN
        self.canPlayRectangle = pygame.Rect(0, 0, 210, 210)

    def onClick(self, none):
        if self.game.selectedCard == self:
            self.game.selectedCard = NULL
        elif self.game.selectedCard == NULL:
            if self.place == 'field' and self.attackUsed == 0:
                if len(self.game.players[self.playerNum == 0].field) == 0:
                    self.attackUsed = 1
                    Arrow(self.game, self.imageHandler.getCenter(), self.game.players[self.playerNum == 0].healthText.position, self.game.players[int(self.playerNum == 0)].healthText.getRect(), self, self.game.players[int(self.playerNum == 0)])
                elif self.stats['Splash'] > 0:
                    self.attackUsed = 1
                    count = 0
                    for card in self.game.players[int(self.playerNum == 0)].field:
                        if count <= self.stats['Splash']:
                            Arrow(self.game, self.imageHandler.getCenter(), card.imageHandler.getCenter(), card.imageHandler.getRect(), self, card)
                            count += 1 
                else:
                    self.game.selectedCard = self
            elif self.place == 'hand' and self.game.players[self.playerNum].mana >= self.stats['Mana'] and self.game.turn == self.playerNum:
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
            self.game.gameObjects.remove(self.statsText[statsText])
        
        self.emptyZone.isFull = 0
        self.game.gameObjects.remove(self.clicker)
        self.game.gameObjects.remove(self.imageHandler)
        self.game.players[self.playerNum].field.remove(self)
        self.game.gameObjects.remove(self)

    def update(self):
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        if self.game.turn == self.playerNum and ((self.place == 'hand' and self.stats['Mana'] <= self.game.players[self.playerNum].mana) or (self.place == 'field' and self.attackUsed == 0)):
            self.canPlayRectangle.x = self.position.x-5
            self.canPlayRectangle.y = self.position.y-5
            pygame.draw.rect(self.game.screen, Colors.GREEN, self.canPlayRectangle, 5)

    def dealDamage(self, target):
        trueDamage = self.stats["Damage"] - target.stats['Armor']
        if trueDamage < 0:
            trueDamage = 0
        target.setHealth(target.stats['Health'] - trueDamage)
        self.setHealth(self.stats['Health'] + self.stats['Drain'])
        if type(target) == type(self):
            FlyingNum(self.game, '- ' + str(trueDamage) + ' health', target.position, Colors.RED)
        if target.stats['Health'] <= 0:
            target.delete()
            self.stats[self.stats['Growth Type']] += 1
            self.statsText[self.stats['Growth Type']].str = self.stats['Growth Type'] + ' ' + str(self.stats[self.stats['Growth Type']])
            FlyingNum(self.game, '+ 1 ' + str(self.stats['Growth Type']), self.position, Colors.GREEN)
    
    def setHealth(self, health):
        self.stats['Health'] = health
        self.statsText['Health'].str = 'Health ' + str(self.stats['Health'])
