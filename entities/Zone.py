from entities.entity import Entity
from components.click_component import ClickComponent
from components.transform_component import TransformComponent

class Zone(Entity):
    def __init__(self, position, playerNum, game):
        super().__init__(game)
        zone_size = 200
        self.transform_component = TransformComponent(game, position, zone_size, zone_size)
        self.isFull = 0
        self.playerNum = playerNum
        self.clicker = ClickComponent((), self)

    def on_click(self):
        selected_card = self.game.currentState['selectedCard']

        if not self.isFull and selected_card != None and self.playerNum == selected_card.playerNum and selected_card.place == 'hand':
            self.isFull = True
            selected_card.place = 'field'
            selected_card.transform_component.position = self.transform_component.position
            selected_card_player = self.game.currentState['players'][selected_card.playerNum]
            selected_card_player.field.append(selected_card)
            selected_card_player.stats['Mana'] -= selected_card.stats['Mana']
            selected_card_player.hand.remove(selected_card)
            selected_card.emptyZone = self
            self.game.currentState['selectedCard'] = None