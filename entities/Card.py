from components.image_component import ImageComponent
from entities.text import TextHandler
from components.transform_component import TransformComponent
from components.click_component import ClickComponent
from entities.entity import Entity
from entities.flying_num import FlyingNum
from entities.arow import Arrow
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
        self.playerNum = playerNum
        self.place = 'hand'
        self.attackUsed = 0
        self.transform_component = TransformComponent(game, (game.SCREEN_WIDTH + 100,0), width=size, height=size)


        filename = 'images/' + self.name.lower() + '.jpg'

        self.imageHandler = ImageComponent(filename, self)

        self.statsText = {}
        for key, value in self.stats.items():
            if key != 'Growth Type' and value != 0:
                self.statsText[key] = TextHandler(game, f'{key} {value}', (0,0), self.game.fonts["medium"])

        self.statsText[self.stats['Growth Type']].color = Colors.LIGHTCYAN
        self.base_health = self.stats['Health']

        self.clicker = ClickComponent((), self)
        self.emptyZone = 0
        self.canPlayRectangle = pygame.Rect(0, 0, 210, 210)
        self.impaledArrows = []

    def on_click(self):
        def attack(attacker, defender):
            attacker.attackUsed = 1
            self.game.currentState['arrowFlies'] = 1
            Arrow(self.game, attacker, defender)
        
        if self.game.currentState['arrowFlies']:
            return

        if self.game.currentState['selectedCard'] == self:
            self.game.currentState['selectedCard'] = None
        elif self.game.currentState['selectedCard'] == None:
            if self.game.currentState['turn'] == self.playerNum:
                player = self.game.currentState['players'][self.playerNum]
                if self.place == 'field' and self.attackUsed == 0:
                    opponent = self.game.currentState['players'][self.playerNum == 0]
                    number_of_cards_on_opponents_field = len(opponent.field)
                    targets = []

                    if  number_of_cards_on_opponents_field == 0:
                        targets = [opponent]
                    elif number_of_cards_on_opponents_field == 1:
                        targets = [opponent.field[0]]
                    elif self.stats['Splash'] > 0:
                        targets = [card for count, card in enumerate(opponent.field) if count <= self.stats['Splash']]
                    else:
                        self.game.currentState['selectedCard'] = self

                    for target in targets:
                        attack(self, target)

                elif self.place == 'hand' and player.mana >= self.stats['Mana']:
                    zone = next((zone for zone in player.zones if not zone.isFull), None)
                    if zone:
                        self.game.currentState['selectedCard'] = self
                        zone.on_click()
        elif self.place == 'field' and self.game.currentState['selectedCard'].place == 'field':
            attack(self.game.currentState['selectedCard'], self)
            self.game.currentState['selectedCard'] = None

    def delete(self):
        for statsText in self.statsText:
            self.statsText[statsText].delete()
        
        self.emptyZone.isFull = 0
        self.game.currentState["gameObjects"].remove(self.clicker)
        self.game.currentState["gameObjects"].remove(self.imageHandler)
        self.game.currentState['players'][self.playerNum].field.remove(self)
        self.game.currentState["gameObjects"].remove(self)

    def update(self):
        font_height = self.game.fonts["medium"].size('A')[1]
        ncount = 0
        for key, value in self.statsText.items():
            self.statsText[key].transform_component.position = self.transform_component.position + pygame.Vector2(5,5 + font_height * ncount)
            ncount += 1

        if self.game.currentState['turn'] == self.playerNum and ((self.place == 'hand' and self.stats['Mana'] <= self.game.currentState['players'][self.playerNum].mana) or (self.place == 'field' and self.attackUsed == 0)):
            outline_thickness = 5
            self.canPlayRectangle.x = self.transform_component.position.x - outline_thickness
            self.canPlayRectangle.y = self.transform_component.position.y - outline_thickness
            pygame.draw.rect(self.game.screen, Colors.LIGHTCYAN, self.canPlayRectangle, 5)

    def dealDamage(self, target):
        true_damage = self.stats["Damage"] - target.stats['Armor']
        true_damage = 0 if true_damage < 0 else true_damage
        
        target.setStat('Health', target.stats['Health'] - true_damage)

        if self.stats['Drain'] > 0:
            self.setStat('Health',self.stats['Health'] + self.stats['Drain'])

        if target.stats['Health'] <= 0:
            i = 0
            for stat in self.stats:
                if stat != 'Growth Type' and stat != 'Mana' and stat != 'Name' and self.stats['Devour'] > i:
                    if stat == 'Health':
                        self.setStat(stat, self.stats[stat] + target.base_health)
                    else:
                        self.setStat(stat, self.stats[stat] + target.stats[stat])
                    i += 1
            
            self.setStat(self.stats['Growth Type'], self.stats[self.stats['Growth Type']] + 1)
            
            for j in target.impaledArrows:
                j.delete()
                
            target.delete()

    def setStat(self, statName, newStat):
        statChange = newStat - self.stats[statName]
        color = Colors.LIGHT_GREEN if statChange > 0 else Colors.LIGHT_RED

        FlyingNum(self.game, str(statChange ) + ' ' + statName, self.transform_component.position, color)
        self.stats[statName] = newStat

        if statName in self.statsText:
            self.statsText[statName].str = statName + ' ' + str(self.stats[statName])
        else:
            self.statsText[statName] = TextHandler(self.game, f'{statName} {newStat}', (0,0), self.game.fonts["medium"])
