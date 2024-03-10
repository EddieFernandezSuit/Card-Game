from asyncio.windows_events import NULL
from components.image_component import ImageComponent
from entities.TextHandler import TextHandler
from components.transform_component import TransformComponent
from components.click_component import ClickComponent
from entities.entity import Entity
from entities.FlyingNum import FlyingNum
from entities.Arrow import Arrow
import pygame
import Colors
import json

class Card(Entity):
    def __init__(self, game, playerNum, name) -> None:
        super().__init__(game)

        cardData = json.load(open('cardData.json'))
        self.stats = cardData[name]
        self.name = name
        size = 200
        self.transform_component = TransformComponent(game, (game.SCREEN_WIDTH + 100,0), width=size, height=size)

        self.playerNum = playerNum
        self.place = 'hand'
        self.attackUsed = 0

        filename = 'images/' + self.name.lower() + '.jpg'

        self.imageHandler = ImageComponent(filename, self)

        self.statsText = {}
        ncount = 0
        font_height = game.fonts["medium"].size('A')[1]
        self.statsText['Name'] = TextHandler(game, self.name, self.transform_component.position, pygame.Vector2(5,5 + font_height * ncount), self.game.fonts["medium"])
        for key, value in self.stats.items():
            if value != 0 and key != 'Growth Type':
                ncount += 1
                self.statsText[key] = TextHandler(game, f'{key} {value}', self.transform_component.position, pygame.Vector2(5,5 + font_height * ncount), self.game.fonts["medium"])

        self.statsText[self.stats['Growth Type']].color = Colors.LIGHTCYAN

        self.clicker = ClickComponent((), self)
        self.emptyZone = 0
        self.canPlayRectangle = pygame.Rect(0, 0, 210, 210)
        self.impaledArrows = []

    def on_click(self):
        def attack(attackingCard, defendingCard):
            attackingCard.attackUsed = 1
            self.game.currentState['arrowFlies'] = 1
            Arrow(self.game, attackingCard, defendingCard)

        if self.game.currentState['arrowFlies'] == 0:
            if self.game.currentState['selectedCard'] == self:
                self.game.currentState['selectedCard'] = NULL
            elif self.game.currentState['selectedCard'] == NULL:
                if self.game.currentState['turn'] == self.playerNum:
                    player = self.game.currentState['players'][self.playerNum]
                    if self.place == 'field' and self.attackUsed == 0:
                        number_of_cards_on_opponents_field = len(self.game.currentState['players'][self.playerNum == 0].field)
                        opponent = self.game.currentState['players'][self.playerNum == 0]
                        targets = []

                        if self.stats['Splash'] > 0:
                            for count, card in enumerate(opponent.field):
                                if count <= self.stats['Splash']:
                                    targets.append(card)
                        elif  number_of_cards_on_opponents_field == 0:
                            targets = [opponent]
                        elif number_of_cards_on_opponents_field == 1:
                            targets = [opponent.field[0]]
                        else:
                            self.game.currentState['selectedCard'] = self

                        for target in targets:
                            attack(self, target)
                    elif self.place == 'hand' and player.mana >= self.stats['Mana']:
                        for zone in player.zones:
                            if not zone.isFull:
                                self.game.currentState['selectedCard'] = self
                                zone.on_click()
                                break
            elif self.place == 'field' and self.game.currentState['selectedCard'].place == 'field':
                attack(self.game.currentState['selectedCard'], self)
                self.game.currentState['selectedCard'] = NULL

    def delete(self):
        for statsText in self.statsText:
            self.statsText[statsText].delete()
        
        self.emptyZone.isFull = 0
        self.game.currentState["gameObjects"].remove(self.clicker)
        self.game.currentState["gameObjects"].remove(self.imageHandler)
        self.game.currentState['players'][self.playerNum].field.remove(self)
        self.game.currentState["gameObjects"].remove(self)

    def update(self):
        # self.transform_component.position.x = self.transform_component.position.x
        # self.transform_component.position.y = self.transform_component.position.y
        if self.game.currentState['turn'] == self.playerNum and ((self.place == 'hand' and self.stats['Mana'] <= self.game.currentState['players'][self.playerNum].mana) or (self.place == 'field' and self.attackUsed == 0)):
            outline_thickness = 5
            self.canPlayRectangle.x = self.transform_component.position.x - outline_thickness
            self.canPlayRectangle.y = self.transform_component.position.y - outline_thickness
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
                            pass
                            # self.statsText[stat] = TextHandler(self.game, stat + ' ' +  str(self.stats[stat]), self.position, pygame.Vector2(5,5 + self.game.fonts['medium'].size('A')[1] * (i+3)), self.game.fonts['medium'])
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

            FlyingNum(self.game, str(statChange ) + ' ' + statName, self.transform_component.position, color)
            self.stats[statName] = newStat
            self.statsText[statName].str = statName + ' ' + str(self.stats[statName]) 
