from entities.entity import Entity
from entities.clickable_text import ClickableText
import pygame

deckUi = {
    'offset': 10,
    'yGap': 30
}

class DeckList(Entity):
    def __init__(self, game, deckName) -> None:
        super().__init__(game)
        self.cards = []
        self.deckName = deckName
        deckNumber = len(game.currentState['deckBox'].deckLists)
        self.nameText = ClickableText(self.game, pygame.Vector2(deckUi['offset'], deckUi['offset'] + deckNumber * deckUi['yGap']), self.onClickDeckName, [game], deckName)
        self.deleteButton = ClickableText(self.game, pygame.Vector2(100, deckUi['offset'] + deckNumber * deckUi['yGap']), self.deleteDeck, [game], 'X')

    def onClickDeckName(self, game):
        self.game.currentState['deckBox'].changeDeck(self)
        pass

    def deleteDeck(self, game):
        game.currentState['deckBox'].deleteDeck(self)
        self.delete()
    
    def on_delete(self):
        self.nameText.delete()
        self.deleteButton.delete()
    
def calc_card_position(game, index):
    return pygame.Vector2(deckUi['offset'], (len(game.currentState['deckBox'].deckLists) + 2) * deckUi['yGap'] + deckUi['offset'] + index * deckUi['yGap'])