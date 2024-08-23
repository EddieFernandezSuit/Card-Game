from entities.entity import Entity
from components.transform_component import TransformComponent
import pygame
from constants import *

class PlayCardRectangle(Entity):
    def on_init(self, card) -> None:
        self.card = card
        self.outline_thickness = 4
        self.transform_component = TransformComponent(self.game, self.card.transform_component.position - (self.outline_thickness, self.outline_thickness), uniform_size=card.size + self.outline_thickness * 2)
        self.color = LIGHTCYAN

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color, self.transform_component.rect, self.outline_thickness)

    def update(self):
        turn = self.game.currentState['turn'] 
        if turn == self.card.playerNum and turn == self.game.currentState['client'].client_id and ((self.card.place == 'hand' and self.card.stats['Mana'] <= self.game.currentState['players'][self.card.playerNum].stats['Mana']) or (self.card.place == 'field' and self.card.attackUsed == 0)):
            self.transform_component.position = self.card.transform_component.position - (self.outline_thickness, self.outline_thickness)
            self.draw()