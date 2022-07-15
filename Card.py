from asyncio.windows_events import NULL
from operator import index
from pstats import Stats
from Handlers.ImageHandler import ImageHandler
from Handlers.TextHandler import TextHandler
from Handlers.Clicker import Clicker
from GameObject import GameObject
from FlyingNum import FlyingNum
from Arrow import Arrow
import pygame
import Colors

class Card(GameObject):
    def __init__(self, game, playerNum, name) -> None:
        super().__init__(game)

        cardStats = [
            ['Name',        'Image Path',   'Growth Type', 'Mana', 'Damage',   'Health',     'Splash',   'Armor',    'Drain'],
            ['Jungle Delver','jungle.jpg',  'Health',       1,      1,          1,                 0,          0,          0],
            ['Bird',        'bird.jpg',     'Damage',       2,      1,          3,                 0,          0,          0],
            ['Turtle',      'turtle.jpg',   'Splash',       3,      2,          4,                 1,          0,          0],
            ['Armordillo',  'armadillo.jpg','Armor',        4,      1,          6,                 0,          1,          0],
            # ['Bats',         'bat.jpg',    'Drain',       5,      4,          6,                  0,          0,          1]
        ]

        addCard = []
        for card in cardStats:
            if card[0].lower() == name.lower():
                addCard = card
                break

        self.game = game
        self.position = pygame.Vector2(-200,0)
        self.imageFilePath = addCard[1]
        self.growthType = addCard[2]
        self.stats = {
            'Name': addCard[0],
            'Mana': addCard[3],
            'Damage': addCard[4],
            'Health': addCard[5],
            'Splash': addCard[6],
            'Armor': addCard[7],
            'Drain': addCard[8],
        }

        self.playerNum = playerNum
        self.place = 'hand'
        self.attackUsed = 0
        self.imageHandler = ImageHandler('images/' + self.imageFilePath, self.position, game)
        self.rect = self.imageHandler.image.get_rect()
        self.clicker = Clicker(self.rect, self.onClick, (), game)
        self.statsText = []
        self.growthIndex = 0

        self.emptyZone = 0
        ncount = 0
        for key in self.stats:
            if key == self.growthType:
                self.growthIndex = ncount
            if self.stats[key] != 0:
                textStr = key + ' ' +  str(self.stats[key])
                if key == 'Name':
                    textStr = str(self.stats[key])
                
                self.statsText.append(TextHandler(game, textStr, 1, self.position, pygame.Vector2(5,5 + game.font.size('A')[1] * ncount) )) 
                ncount += 1

        self.statsText[self.growthIndex].color = Colors.LIGHTCYAN
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
            self.game.gameObjects.remove(statsText)
        
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
        if type(target) == type(self):
            FlyingNum(self.game, '- ' + str(trueDamage) + ' health', target.position, Colors.RED)
        if target.stats['Health'] <= 0:
            target.delete()
            self.stats[self.growthType] += 1
            self.statsText[self.growthIndex].str = self.growthType + ' ' + str(self.stats[self.growthType])
            FlyingNum(self.game, '+ 1 ' + str(self.growthType), self.position, Colors.GREEN)
    
    def setHealth(self, health):
        self.stats['Health'] = health
        self.statsText[3].str = 'Health ' + str(self.stats['Health'])
