from asyncio.windows_events import NULL
from Handlers.ImageHandler import ImageHandler
from Handlers.TextHandler import TextHandler
from Handlers.ClickHandler import Clicker
from GameObjects.GameObject import GameObject
from GameObjects.FlyingNum import FlyingNum
from GameObjects.Arrow import Arrow
import pygame
import Colors
import json

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

        self.statsText = {}
        ncount = 0
        self.statsText['Name'] = TextHandler(game, self.name, self.position, pygame.Vector2(5,5 + game.states[game.currentState]['smallFont'].size('A')[1] * ncount), self.game.states[game.currentState]['smallFont'])
        for key in self.stats:
            if self.stats[key] != 0 and key != 'Growth Type':
                ncount += 1
                self.statsText[key] = TextHandler(game, key + ' ' +  str(self.stats[key]), self.position, pygame.Vector2(5,5 + game.states[game.currentState]['smallFont'].size('A')[1] * ncount), self.game.states[game.currentState]['smallFont'])

        self.statsText[self.stats['Growth Type']].color = Colors.LIGHTCYAN

        self.clicker = Clicker(self.rect, self.onClick, (), game)
        self.emptyZone = 0
        self.canPlayRectangle = pygame.Rect(0, 0, 210, 210)
        self.impaledArrows = []

    def onClick(self, none):

        def attack(attackingCard, defendingCard):
            attackingCard.attackUsed = 1
            self.game.states[self.game.currentState]['arrowFlies'] = 1
            Arrow(self.game, attackingCard, defendingCard)

        if self.game.states[self.game.currentState]['arrowFlies'] == 0:
            if self.game.states[self.game.currentState]['selectedCard'] == self:
                self.game.states[self.game.currentState]['selectedCard'] = NULL
            elif self.game.states[self.game.currentState]['selectedCard'] == NULL:
                if self.game.states[self.game.currentState]['turn'] == self.playerNum:
                    if self.place == 'field' and self.attackUsed == 0:
                        if len(self.game.states[self.game.currentState]['players'][self.playerNum == 0].field) == 0:
                            attack(self, self.game.states[self.game.currentState]['players'][self.playerNum == 0])
                        elif len(self.game.states[self.game.currentState]['players'][self.playerNum == 0].field) == 1:
                            attack(self, self.game.states[self.game.currentState]['players'][self.playerNum == 0].field[0])
                        elif self.stats['Splash'] > 0:
                            self.attackUsed = 1
                            self.game.states[self.game.currentState]['arrowFlies'] = 1
                            count = 0
                            for card in self.game.states[self.game.currentState]['players'][int(self.playerNum == 0)].field:
                                if count <= self.stats['Splash']:
                                    Arrow(self.game.states[self.game.currentState], self, card)
                                    count += 1 
                        else:
                            self.game.states[self.game.currentState]['selectedCard'] = self
                    elif self.place == 'hand' and self.game.states[self.game.currentState]['players'][self.playerNum].mana >= self.stats['Mana']:
                        for zone in self.game.states[self.game.currentState]['players'][self.playerNum].zones:
                            if zone.isFull == 0:
                                self.game.states[self.game.currentState]['selectedCard'] = self
                                zone.click(self.game)
                                break
                
            elif self.place == 'field' and self.game.states[self.game.currentState]['selectedCard'].place == 'field':
                attack(self.game.states[self.game.currentState]['selectedCard'], self)
                self.game.states[self.game.currentState]['selectedCard'] = NULL

    def delete(self):
        for statsText in self.statsText:
            self.statsText[statsText].delete()
        
        self.emptyZone.isFull = 0
        self.game.states[self.game.currentState].gameObjects.remove(self.clicker)
        self.game.states[self.game.currentState].gameObjects.remove(self.imageHandler)
        self.game.states[self.game.currentState]['players'][self.playerNum].field.remove(self)
        self.game.states[self.game.currentState].gameObjects.remove(self)

    def update(self):
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        if self.game.states[self.game.currentState]['turn'] == self.playerNum and ((self.place == 'hand' and self.stats['Mana'] <= self.game.states[self.game.currentState]['players'][self.playerNum].mana) or (self.place == 'field' and self.attackUsed == 0)):
            self.canPlayRectangle.x = self.position.x-5
            self.canPlayRectangle.y = self.position.y-5
            pygame.draw.rect(self.game.screen, Colors.LIGHTCYAN, self.canPlayRectangle, 5)

    def dealDamage(self, target):
        trueDamage = self.stats["Damage"] - target.stats['Armor']
        if trueDamage < 0:
            trueDamage = 0
        targetHealthBeforeDeath = target.stats['Health']
        target.setStat('Health', target.stats['Health'] - trueDamage)
        self.setStat('Health',self.stats['Health'] + self.stats['Drain'])
        if target.stats['Health'] <= 0:
            i = 0
            for stat in self.stats:
                if stat != 'Growth Type' and stat != 'Mana':
                    if self.stats['Devour'] > i:
                        found = False
                        for statText in self.statsText:
                            if statText == stat:
                                found = True
                        if found == False:
                            self.statsText[stat] = TextHandler(self.game, stat + ' ' +  str(self.stats[stat]), 1, self.position, pygame.Vector2(5,5 + self.game.states[self.game.currentState]['smallFont'].size('A')[1] * (i+3)), self.game.states[self.game.currentState]['smallFont'])
                        if stat == 'Health':
                            self.setStat(stat, self.stats[stat] + targetHealthBeforeDeath)
                        else:
                            self.setStat(stat, self.stats[stat] + target.stats[stat])
                        i += 1
                    else:
                        break
            self.setStat(self.stats['Growth Type'], self.stats[self.stats['Growth Type']] + 1)
            
            for j in target.impaledArrows:
                j.delete()
                
            target.delete()

    def setStat(self, statName, newStat):
        statChange = newStat - self.stats[statName]
        if statChange != 0:
            color = ''
            if statChange < 0: color = Colors.RED
            elif statChange > 0: color = Colors.GREEN

            FlyingNum(self.game, str(statChange ) + ' ' + statName, self.position, color)
            self.stats[statName] = newStat
            self.statsText[statName].str = statName + ' ' + str(self.stats[statName]) 
