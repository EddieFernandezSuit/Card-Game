from entities.entity import Entity
from components.click_component import ClickComponent
from components.transform_component import TransformComponent

class Zone(Entity):
    def __init__(self, position, playerNum, game):
        super().__init__(game)
        self.transform_component = TransformComponent(game, position, 200, 200)
        self.isFull = 0
        self.playerNum = playerNum
        self.clicker = ClickComponent((), self)

    def on_click(self):
        if self.isFull == 0 and self.game.currentState['selectedCard'] != None and self.playerNum == self.game.currentState['selectedCard'].playerNum and self.game.currentState['selectedCard'].place == 'hand':
            self.game.currentState['selectedCard'].place = 'field'
            self.game.currentState['players'][self.game.currentState['selectedCard'].playerNum].field.append(self.game.currentState['selectedCard'])
            self.game.currentState['selectedCard'].transform_component.position.x = self.transform_component.position.x
            self.game.currentState['selectedCard'].transform_component.position.y = self.transform_component.position.y
            self.isFull = 1
            self.game.currentState['players'][self.game.currentState['selectedCard'].playerNum].mana -= self.game.currentState['selectedCard'].stats['Mana']
            for k in range(len(self.game.currentState['players'][self.game.currentState['selectedCard'].playerNum].hand)):
                if self.game.currentState['players'][self.game.currentState['selectedCard'].playerNum].hand[k] == self.game.currentState['selectedCard']:
                    self.game.currentState['players'][self.game.currentState['selectedCard'].playerNum].hand.pop(k)
                    break
            self.game.currentState['selectedCard'].emptyZone = self
            self.game.currentState['selectedCard'] = None