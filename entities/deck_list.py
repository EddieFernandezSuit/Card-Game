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
        self.nameText = ClickableText(self.game, pygame.Vector2(deckUi['offset'], deckUi['offset'] + deckNumber * deckUi['yGap']), self.onClickDeckName, [game], deckName, self.game.fonts['medium'])
    
    def onClickDeckName(self, game):
        self.game.currentState['deckBox'].changeDeck(self)
        pass

    def delete(self):
        super().delete()
        del self.nameText
    
def calculateCardPosition(game, index):
    return pygame.Vector2(deckUi['offset'], (len(game.currentState['deckBox'].deckLists) + 2) * deckUi['yGap'] + deckUi['offset'] + index * deckUi['yGap'])