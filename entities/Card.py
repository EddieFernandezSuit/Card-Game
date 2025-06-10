from components.stats_component import StatsComponent
from components.image_component import ImageComponent
from entities.text import Text
from components.transform_component import TransformComponent
from components.click_component import ClickComponent
from entities.entity import Entity
from entities.arow import Arrow
from entities.play_card_rectangle import PlayCardRectangle
from constants import *
import Timer
import pygame
import json
import datetime

class Card(Entity):
    def on_init(self, playerNum, name) -> None:
        card_data = json.load(open('cardData.json'))
        self.name = name
        self.stats = card_data[name]
        self.stats['base_health'] = self.stats['Health']
        self.playerNum = playerNum
        self.place = 'hand'
        self.attackUsed = 0
        self.recoil_timer = None
        self.size = CARD_SIZE
        self.arrow_woosh_sound = pygame.mixer.Sound('sounds/arrow_woosh.mp3')
        self.emptyZone = 0
        self.impaledArrows = []
        filename = 'images/' + name.lower() + '.jpg'

        self.add_components(
            TransformComponent(self.game, (self.game.SCREEN_WIDTH + 100,0), width=self.size, height=self.size),
            ImageComponent(self.game, filePath=filename, entity=self, scaled_size=self.size),
            ClickComponent(entity=self),
            StatsComponent(self, self.stats)
        )

        self.statsText = {key: Text(self.game, f'{value}' if key == 'Name' else f'{value} {key}', font_size='small')
            for key, value in self.stats.items() 
            if key != 'Growth Type' and value != 0 and key != 'base_health'}

        self.statsText[self.stats['Growth Type']].color = LIGHTCYAN
        # self.statsText['Health'].color = GREEN
        # self.statsText['Damage'].color = RED

        self.play_rectangle = PlayCardRectangle(self.game, self)

    def on_click(self):        
        if self.game.currentState['arrowFlies']:
            return

        if self.game.currentState['selectedCard'] == self:
            self.game.currentState['selectedCard'] = None
        elif self.game.currentState['selectedCard'] == None:
            turn = self.game.currentState['turn'] 
            if turn == self.playerNum and turn == self.game.currentState['client'].client_id:
                player = self.game.currentState['players'][self.playerNum]
                if self.place == 'field' and self.attackUsed == 0:
                    opponent = self.game.get_opponent(self.game)
                    number_of_cards_on_opponents_field = len(opponent.field)
                    targets = []

                    if self.stats['Splash'] > 0: targets = [card for count, card in enumerate(opponent.field) if count <= self.stats['Splash']]
                    if number_of_cards_on_opponents_field == 0: targets = [opponent]
                    if number_of_cards_on_opponents_field == 1: targets = [opponent.field[0]]
                    if not targets: self.game.currentState['selectedCard'] = self

                    for target in targets:
                        self.send_attacker_message(self, target, self.playerNum)
                        self.attack(target)

                elif self.place == 'hand' and player.stats['Mana'] >= self.stats['Mana']:
                    self.play()
                    play_message = {'play': self.name}
                    self.game.send(play_message)

        elif self.place == 'field' and self.game.currentState['selectedCard'].place == 'field':
            self.send_attacker_message(self.game.currentState['selectedCard'], self, self.playerNum==0)
            self.game.currentState['selectedCard'].attack(self)

    def send_attacker_message(self, attacker, defender, attacking_player_num):
        print(attacker, defender, attacking_player_num)
        attacker_field_id = attacker.get_field_id(attacking_player_num)
        defender_field_id = 'player'
        defending_player_num = attacking_player_num == 0

        if type(defender).__name__ == 'Card':
            defender_field_id = defender.get_field_id(defending_player_num)
        
        attack_message = {'attacker': {'player_num': attacking_player_num, 'field_id': attacker_field_id}, 'defender': {'player_num': defending_player_num, 'field_id': defender_field_id}}
        self.game.send(attack_message)
    
    def send_multi_target_attack(self, targets):
        attack_message = {
            'attacker': {
                'player_num': self.playerNum,
                'field_id': self.get_field_id()
            },
            'multiple_targets': []
        }
        for target in targets:
           if isinstance(target, Card):
                attack_message['multiple_targets'].append({'player_num': target.playerNum == 0, 'field_id': target.get_field_id()})
           else:
                attack_message['multiple_targets'].append({'player_num': target.playerNum == 0, 'field_id': 'player'})
        
        self.game.send(attack_message) 

    def get_field_id(self, player_num):
        id = 0
        for index, card in enumerate(self.game.currentState['players'][player_num].field):
            if self == card:
                return index
        return id

    def play(self):
        player = self.game.currentState['players'][self.playerNum]
        flip_card_sound = pygame.mixer.Sound('sounds/flip_card.mp3')
        flip_card_sound.set_volume(self.game.volume)
        flip_card_sound.play()

        self.handle_bird_sound()
        zone = next((zone for zone in player.zones if not zone.isFull), None)
        if zone:
            self.game.currentState['selectedCard'] = self
            zone.on_click()

    def handle_bird_sound(self):
        BIRD_SOUND_FILE = 'sounds/bird.mp3'
        if self.stats['Name'] == 'Bird':
            bird_sound = pygame.mixer.Sound(BIRD_SOUND_FILE)
            bird_sound.set_volume(self.game.volume)
            bird_sound.play()
            # pygame.mixer.Sound(BIRD_SOUND_FILE).play()

    def on_delete(self):
        for statsText in self.statsText:
            self.statsText[statsText].delete()

        for arrow in self.impaledArrows:
            arrow.delete()

        self.emptyZone.isFull = 0
        self.game.currentState['players'][self.playerNum].field.remove(self)
        self.play_rectangle.delete()

    def update(self):
        font_height = self.statsText['Name'].height
        ncount = 0
        try:
            for key, value in self.statsText.items():
                self.statsText[key].transform_component.position = self.transform_component.position + pygame.Vector2(5,5 + font_height * ncount)
                ncount += 1
        except Exception as e:
            print(e)
            print(self)
        if self.recoil_timer:
            self.recoil_timer.update()

    def deal_damage(self, target):
        true_damage = max(0, self.stats["Damage"] - target.stats['Armor'])
        target.stats_component.set_stat('Health', target.stats['Health'] - true_damage)

        if self.stats['Drain'] > 0:
            self.stats_component.set_stat('Health',self.stats['Health'] + self.stats['Drain'])
        
        if target.stats['Health'] <= 0:
            devourable_stats = [stat for stat in list(self.stats) if stat not in ['Growth Type', 'Mana', 'Name', 'base_health'] and self.stats[stat] > 0][:self.stats['Devour']]
            for stat in devourable_stats:
                if 'base_health' in target.stats:
                    self.stats_component.set_stat(stat, self.stats[stat] + (target.stats['base_health'] if stat == 'Health' else target.stats[stat]))
            
            self.stats_component.set_stat(self.stats['Growth Type'], self.stats[self.stats['Growth Type']] + 1)
            target.delete()

    def attack(self, target):
        self.attackUsed = 1
        self.game.currentState['arrowFlies'] = 1
        self.game.currentState['selectedCard'] = None
        self.arrow_woosh_sound.play()
        self.handle_bird_sound()
        arrow = Arrow(self.game, self, target)
        self.before_position = self.transform_component.position
        self.transform_component.direction = -arrow.transform_component.direction
        self.transform_component.speed = 2

        def stop():
            self.transform_component.speed = 0
            self.recoil_timer = None
            self.transform_component.position = self.before_position

        def go_back():
            self.transform_component.direction = arrow.transform_component.direction
            self.recoil_timer = Timer.Timer(5,stop)

        self.recoil_timer = Timer.Timer(5,go_back)
        