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
            ['Name',        'Image Path',   'Mana', 'Damage',   'Health',   'Growth Type',  'Splash',   'Armor',    'Drain'],
            ['Jungle Delver','jungle.jpg',  1,      1,          1,          'health',       0,          0,          0],
            ['Bird',        'bird.jpg',     2,      1,          3,          'damage',       0,          0,          0],
            ['Turtle',      'turtle.jpg',   3,      2,          4,          'splash',       1,          0,          0],
            ['Armordillo',  'armadillo.jpg',4,      1,          6,          'armor',        0,          1,          0],
            # ['Bats',         'bat.jpg',     5,      4,          6,          'Drain',        0,          0,          1]
        ]

        addCard = []
        for card in cardStats:
            if card[0].lower() == name.lower():
                addCard = card
                break

        self.game = game
        self.position = pygame.Vector2(-200,0)
        self.name = name
        self.imageFilePath = addCard[1]
        self.mana = addCard[2]
        self.damage = addCard[3]
        self.health = [addCard[4]]
        self.growthType = addCard[5]
        self.splash = addCard[6]
        self.armor = addCard[7]
        self.drain = addCard[8]
        self.stats = {
            'Name': addCard[0],
            'Mana': addCard[2],
            'Damage': addCard[3],
            'Health': addCard[4],
            'Splash': addCard[6],
            'Armor': addCard[7],
            'Drain': addCard[8],
        }

        self.growthStat = self.health
        self.playerNum = playerNum
        self.place = 'hand'
        self.fieldPosition = 0
        self.attackUsed = 0
        self.imageHandler = ImageHandler('images/' + self.imageFilePath, self.position, game)
        self.rect = self.imageHandler.image.get_rect()
        self.clicker = Clicker(self.rect, self.onClick, (), game)
        # self.statsStr = [self.name, 'Mana ' + str(self.mana), 'Damage ' + str(self.damage), 'Health ' + str(self.health[0])]
        self.statsText = []

        self.growthStats ={
            'damage': 2,
            'health': 3,
        }
        count = 4
        if self.splash > 0:
            # self.statsStr.append('Splash '+str(self.splash))
            self.growthStats['splash'] = count
            count+=1
        if self.armor > 0:
            # self.statsStr.append('Armor ' + str(self.armor))
            self.growthStats['armor'] = count
            count +=1
        if self.drain > 0:
            # self.statsStr.append('Drain ' + str(self.drain))
            self.growthStats['drain'] = count
            count+=1

        self.emptyZone = 0

        # for index, statStr in enumerate(self.statsStr):
        #     self.statsText.append(TextHandler(game, statStr, 1, self.position, pygame.Vector2(5,5 + game.font.size(statStr)[1] * index)))
        
        ncount = 0

        for key in self.stats:
            if self.stats[key] != 0:
                textStr = key + ' ' +  str(self.stats[key])
                if key == 'Name':
                    textStr = str(self.stats[key])
                
                self.statsText.append(TextHandler(game, textStr, 1, self.position, pygame.Vector2(5,5 + game.font.size('A')[1] * ncount) )) 
                ncount += 1

        self.statsText[self.growthStats[self.growthType]].color = Colors.LIGHTCYAN
        self.canPlayRectangle = pygame.Rect(0, 0, 210, 210)

    def onClick(self, none):
        if self.game.selectedCard == self:
            self.game.selectedCard = NULL
        elif self.game.selectedCard == NULL:
            if self.place == 'field' and self.attackUsed == 0:
                if len(self.game.players[self.playerNum == 0].field) == 0:
                    self.attackUsed = 1
                    Arrow(self.game, self.imageHandler.getCenter(), self.game.players[self.playerNum == 0].healthText.position, self.game.players[int(self.playerNum == 0)].healthText.getRect(), self, self.game.players[int(self.playerNum == 0)])
                elif self.splash > 0:
                    self.attackUsed = 1
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
        # self.statsText[3].str = 'H ' + str(self.health[0])

        if self.game.turn == self.playerNum and ((self.place == 'hand' and self.mana <= self.game.players[self.playerNum].mana) or (self.place == 'field' and self.attackUsed == 0)):
            self.canPlayRectangle.x = self.position.x-5
            self.canPlayRectangle.y = self.position.y-5
            pygame.draw.rect(self.game.screen, Colors.GREEN, self.canPlayRectangle, 5)


    def dealDamage(self, target):
        trueDamage = self.damage - target.armor
        if trueDamage < 0:
            trueDamage = 0
        target.health[0] -= trueDamage
        if type(target) == type(self):
            FlyingNum(self.game, '- ' + str(trueDamage) + ' health', target.position, Colors.RED)
        if target.health[0] <= 0:
            target.delete()
            if self.growthType == 'health':
                self.growthStat[0] += 1
            else:
                growthStatName = self.growthType + ' '
                gStat = 0
                if self.growthType == 'damage':
                    self.damage += 1
                    gStat = self.damage
                elif self.growthType == 'splash':
                    self.splash += 1
                    gStat = self.splash
                elif self.growthType == 'armor':
                    self.armor += 1
                    gStat = self.armor

                self.statsText[self.growthStats[self.growthType]].str = self.growthType + ' ' + str(gStat)
            FlyingNum(self.game, '+ 1 ' + str(self.growthType), self.position, Colors.GREEN)
            
