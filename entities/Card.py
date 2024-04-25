from components.stats_component import StatsComponent
from components.image_component import ImageComponent
from entities.text import Text
from components.transform_component import TransformComponent
from components.click_component import ClickComponent
from entities.entity import Entity
from entities.flying_num import FlyingNum
from entities.arow import Arrow
from entities.play_card_rectangle import PlayCardRectangle
from constants import *
import pygame
import json

class Card(Entity):
    def on_init(self, playerNum, name) -> None:
        card_data = json.load(open('cardData.json'))
        self.stats = card_data[name]
        self.stats['base_health'] = self.stats['Health']
        self.playerNum = playerNum
        self.place = 'hand'
        self.attackUsed = 0
        self.size = 200
        self.arrow_woosh_sound = pygame.mixer.Sound('sounds/arrow_woosh.mp3')
        self.emptyZone = 0
        self.impaledArrows = []
        filename = 'images/' + name.lower() + '.jpg'

        self.add_components([
            TransformComponent(self.game, (self.game.SCREEN_WIDTH + 100,0), width=self.size, height=self.size),
            ImageComponent(filePath=filename, entity=self),
            ClickComponent(entity=self),
            StatsComponent(self, self.stats)
        ])

        self.statsText = {key: Text(self.game, f'{value}' if key == 'Name' else f'{key} {value}')
            for key, value in self.stats.items() 
            if key != 'Growth Type' and value != 0 and key != 'base_health'}

        self.statsText[self.stats['Growth Type']].color = LIGHTCYAN

        self.play_rectangle = PlayCardRectangle(self.game, self)

    def on_click(self):
        def attack(attacker, defender):
            attacker.attackUsed = 1
            self.game.currentState['arrowFlies'] = 1
            self.arrow_woosh_sound.play()
            if self.stats['Name'] == 'Bird':
                pygame.mixer.Sound('sounds/bird.mp3').play()
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

                    if self.stats['Splash'] > 0: targets = [card for count, card in enumerate(opponent.field) if count <= self.stats['Splash']]
                    if number_of_cards_on_opponents_field == 0: targets = [opponent]
                    if number_of_cards_on_opponents_field == 1: targets = [opponent.field[0]]
                    if not targets:self.game.currentState['selectedCard'] = self

                    for target in targets:
                        attack(self, target)

                elif self.place == 'hand' and player.stats['Mana'] >= self.stats['Mana']:
                    pygame.mixer.Sound('sounds/flip_card.mp3').play()
                    if self.stats['Name'] == 'Bird':
                        pygame.mixer.Sound('sounds/bird.mp3').play()
                    zone = next((zone for zone in player.zones if not zone.isFull), None)
                    if zone:
                        self.game.currentState['selectedCard'] = self
                        zone.on_click()

        elif self.place == 'field' and self.game.currentState['selectedCard'].place == 'field':
            attack(self.game.currentState['selectedCard'], self)
            self.game.currentState['selectedCard'] = None
        

    def on_delete(self):
        for statsText in self.statsText:
            self.statsText[statsText].delete()

        for arrow in self.impaledArrows:
            arrow.delete()

        self.emptyZone.isFull = 0
        self.game.currentState['players'][self.playerNum].field.remove(self)
        self.play_rectangle.delete()

    def update(self):
        font_height = self.game.fonts["medium"].size('A')[1]
        ncount = 0
        for key, value in self.statsText.items():
            self.statsText[key].transform_component.position = self.transform_component.position + pygame.Vector2(5,5 + font_height * ncount)
            ncount += 1

    def deal_damage(self, target):
        true_damage = max(0, self.stats["Damage"] - target.stats['Armor'])
        
        target.stats_component.set_stat('Health', target.stats['Health'] - true_damage)

        if self.stats['Drain'] > 0:
            self.stats_component.set_stat('Health',self.stats['Health'] + self.stats['Drain'])
        
        if target.stats['Health'] <= 0:
            devourable_stats = [stat for stat in list(self.stats) if stat not in ['Growth Type', 'Mana', 'Name', 'base_health'] and self.stats[stat] > 0][:self.stats['Devour']]
            for stat in devourable_stats:
                self.stats_component.set_stat(stat, self.stats[stat] + (target.stats['base_health'] if stat == 'Health' else target.stats[stat]))
            
            self.stats_component.set_stat(self.stats['Growth Type'], self.stats[self.stats['Growth Type']] + 1)
            
            target.delete()
