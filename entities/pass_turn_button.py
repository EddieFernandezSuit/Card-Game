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
        self.imageHandler = ImageComponent('images/PassTurn.png', self)
        self.clicker = ClickComponent((), self)
        self.turnRectangleY = [0, 450]

    def on_click(self):
        self.game.currentState['selectedCard'] = None
        for player in self.game.currentState['players']:
            for card in player.field:
                card.attackUsed = 0
        
        self.game.currentState['turn'] = int(self.game.currentState['turn'] == 0)
        self.game.currentState['players'][self.game.currentState['turn']].totalMana += 1
        self.game.currentState['players'][self.game.currentState['turn']].setMana(self.game.currentState['players'][self.game.currentState['turn']].totalMana)

        if len(self.game.currentState['players'][self.game.currentState['turn']].hand) < 5 and len(self.game.currentState['players'][self.game.currentState['turn']].deck) > 0:
            self.game.currentState['players'][self.game.currentState['turn']].drawCard()
        self.game.currentState['turnRectangle'].y = self.turnRectangleY[self.game.currentState['turn']]



