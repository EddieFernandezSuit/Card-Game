from entities.entity import Entity
import pygame
from components.image_component import ImageComponent
from components.click_component import ClickComponent
from components.transform_component import TransformComponent

class PassTurnButton(Entity):
    def __init__(self, game):
        super().__init__(game)
        self.handlers = []
        size = 100
        self.transform_component = TransformComponent(game, pygame.Vector2(game.SCREEN_WIDTH - 200, game.SCREEN_HEIGHT/2 - 50), width=size, height=size)
        file_path = 'images/'
        file_path += 'pass_turn_cyan.png' if self.game.currentState['client'].client_id == 0 else 'PassTurn.png'
        self.image_component = ImageComponent(game, filePath=file_path, entity=self)
        self.click_component = ClickComponent((), self)
        self.y_position_turn_rectangle = [0, 450]
        self.sound = pygame.mixer.Sound('sounds/metal_card_shuffle.wav')
        

    def on_click(self):
        if self.game.currentState['client'].client_id == self.game.currentState['turn']:
            self.pass_turn()
            pass_message = {'pass': True}
            self.game.send(pass_message)

    def on_delete(self):
        self.transform_component.delete()
        self.image_component.delete()
        self.click_component.delete()
    
    def pass_turn(self):
        self.game.currentState['selectedCard'] = None
        self.sound.set_volume(self.game.volume)
        self.sound.play()
        for player in self.game.currentState['players']:
            for card in player.field:
                card.attackUsed = 0

        self.game.currentState['turn'] = self.game.currentState['turn'] == 0
        file_path = 'images/'
        file_path += 'pass_turn_cyan.png' if self.game.currentState['turn'] == self.game.currentState['client'].client_id else 'PassTurn.png'
        self.image_component.set_image(file_path)

        turn = self.game.currentState['turn']
        turn_player = self.game.currentState['players'][turn]
        turn_player.totalMana += 1
        turn_player.stats_component.set_stat('Mana', turn_player.totalMana)

        if len(turn_player.hand) < 5 and turn_player.deck:
            turn_player.draw_card()

