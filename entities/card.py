from components.stats_component import StatsComponent
from components.image_component import ImageComponent
from entities.text import Text
from components.transform_component import TransformComponent
from components.click_component import ClickComponent
from entities.entity import Entity
from entities.arrow import Arrow
from entities.play_card_rectangle import PlayCardRectangle
from entities.selected_text import SelectedCardMarker
from constants import *
from paths import asset_path, data_path
import timer
import pygame
import json
import datetime

class Card(Entity):
    def on_init(self, playerNum, name) -> None:
        card_data = json.load(open(data_path('card_data.json')))
        self.name = name
        self.stats = card_data[name]
        self.stats['base_health'] = self.stats['Health']
        self.playerNum = playerNum
        self.place = 'hand'
        self.attackUsed = 0
        self.recoil_timer = None
        self.size = CARD_SIZE
        self.arrow_woosh_sound = pygame.mixer.Sound(asset_path('sounds/arrow_woosh.mp3'))
        self.emptyZone = 0
        self.impaledArrows = []
        filename = asset_path('images', name.lower() + '.jpg')

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
        # Created last so it is drawn after this card's image, otherwise the
        # card covers the selected marker
        self.selected_marker = SelectedCardMarker(self.game, self)

    def on_click(self):        
        if self.game.currentState.arrowFlies:
            return

        if self.game.currentState.selectedCard == self:
            self.game.currentState.selectedCard = None
        elif self.game.currentState.selectedCard == None:
            turn = self.game.currentState.turn 
            if turn == self.playerNum and turn == self.game.currentState.client.client_id:
                player = self.game.currentState.players[self.playerNum]
                if self.place == 'field' and self.attackUsed == 0:
                    targets = self.get_attack_targets()
                    if targets:
                        self.send_attack_message(targets)
                        self.attack(targets)
                    else:
                        # No splash targets: let the player pick one manually.
                        self.game.currentState.selectedCard = self

                elif self.place == 'hand' and player.stats['Mana'] >= self.stats['Mana']:
                    self.play()
                    play_message = {'play': self.name}
                    self.game.send(play_message)

        elif (self.place == 'field'
              and self.game.currentState.selectedCard.place == 'field'
              and self.playerNum != self.game.currentState.selectedCard.playerNum):
            attacker = self.game.currentState.selectedCard
            attacker.send_attack_message([self])
            attacker.attack([self])

    def get_attack_targets(self):
        """Targets this card hits when clicked without a manual selection.

        An empty list means the player has to click a target themselves.
        """
        opponent = self.game.get_opponent(self.game)
        enemy_cards = opponent.field

        if not enemy_cards:
            return [opponent]

        splash = self.stats.get('Splash', 0)
        if splash > 0:
            return enemy_cards[:splash + 1]

        if len(enemy_cards) == 1:
            return [enemy_cards[0]]

        return []

    def send_attack_message(self, targets):
        """Send one message for the whole attack, including splash targets."""
        defending_player_num = 1 - self.playerNum
        target_payload = []
        for target in targets:
            if isinstance(target, Card):
                field_id = target.get_field_id(defending_player_num)
            else:
                field_id = 'player'
            target_payload.append({'player_num': defending_player_num, 'field_id': field_id})

        self.game.send({
            'attacker': {
                'player_num': self.playerNum,
                'field_id': self.get_field_id(self.playerNum),
            },
            'targets': target_payload,
        })

    def get_field_id(self, player_num):
        for index, card in enumerate(self.game.currentState.players[player_num].field):
            if self == card:
                return index
        return 0

    def play(self):
        player = self.game.currentState.players[self.playerNum]
        flip_card_sound = pygame.mixer.Sound(asset_path('sounds/flip_card.mp3'))
        flip_card_sound.set_volume(self.game.volume)
        flip_card_sound.play()

        self.handle_bird_sound()
        zone = next((zone for zone in player.zones if not zone.isFull), None)
        if zone:
            self.game.currentState.selectedCard = self
            zone.on_click()

    def handle_bird_sound(self):
        BIRD_SOUND_FILE = asset_path('sounds/bird.mp3')
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
        self.game.currentState.players[self.playerNum].field.remove(self)
        self.play_rectangle.delete()
        self.selected_marker.delete()

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
            i = 0
            for stat in devourable_stats:
                if 'base_health' in target.stats:
                    i += 1

                    self.stats_component.set_stat(stat, self.stats[stat] + (target.stats['base_health'] if stat == 'Health' else target.stats[stat]), delay=i * 1000)
            
            self.stats_component.set_stat(self.stats['Growth Type'], self.stats[self.stats['Growth Type']] + 1)
            target.delete()

    def attack(self, targets):
        targets = list(targets)
        if not targets:
            return

        self.attackUsed = 1
        # Count arrows so the board stays locked until every splash arrow has
        # landed instead of unlocking when the first one hits.
        self.game.currentState.arrowFlies += len(targets)
        self.game.currentState.selectedCard = None
        self.arrow_woosh_sound.play()
        self.handle_bird_sound()
        arrows = [Arrow(self.game, self, target) for target in targets]
        # Copy: TransformComponent mutates its position Vector2 in place.
        self.before_position = self.transform_component.position.copy()
        self.transform_component.direction = -arrows[0].transform_component.direction
        self.transform_component.speed = 2

        def stop():
            self.transform_component.speed = 0
            self.recoil_timer = None
            self.transform_component.position = self.before_position

        def go_back():
            self.transform_component.direction = arrows[0].transform_component.direction
            self.recoil_timer = timer.Timer(5,stop)

        self.recoil_timer = timer.Timer(5,go_back)
        