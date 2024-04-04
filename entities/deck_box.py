from entities.entity import Entity
from entities.deck_list import DeckList
from entities.clickable_text import ClickableText
from entities.deck_list import calc_card_position
from entities.deck_list import deckUi
from entities.text import Text
import pygame

class DeckBox(Entity):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.deckLists = []
        self.textCardsInSelectedDeck = []
        self.AddDeckButton = ClickableText(game, pygame.Vector2(10, 10), self.addDeck, [], 'Add Deck')
        position = pygame.Vector2(deckUi['offset'], deckUi['offset'] + 5 * deckUi['yGap'])
        self.selectedDeckText = Text(game, 'Deck 0', position)
        self.selectedDeckList = {}
    
    def changeDeck(self, deckList):
        for text in self.textCardsInSelectedDeck:
            text.delete()
        
        self.textCardsInSelectedDeck = []
        self.selectedDeckText.str = deckList.deckName
        self.selectedDeckList = deckList

        for j, card in enumerate(deckList.cards):
            i = j + 2
            self.textCardsInSelectedDeck.append(ClickableText(self.game, calc_card_position(self.game, i), self.removeOneCard, [card['name']], str(card['quantity']) + ' ' + card['name']))
        
    def addDeck(self):
        deckName = 'Deck ' + str(len(self.deckLists))
        deckList = DeckList(self.game, deckName)
        self.changeDeck(deckList)
        self.deckLists.append(self.selectedDeckList)
        self.AddDeckButton.text.transform_component.position.y = 10 + len(self.deckLists) * 30
        self.selectedDeckText.transform_component.position.y = 10 + (len(self.deckLists) + 3) * 30
        self.updateCardUiPosition()
        return deckList
    
    def findIndexDictionary(self, key, value):
        for i, dict in enumerate(self.selectedDeckList.cards):
            if dict[key] == value:
                return i
        return -1

    def addCard(self, cardName):
        index = self.findIndexDictionary('name', cardName)
        if index == -1:
            self.selectedDeckList.cards.append({'quantity': 1, 'name': cardName})
            self.textCardsInSelectedDeck.append(ClickableText(self.game, calc_card_position(self.game, len(self.selectedDeckList.cards) + 1), self.removeOneCard, [cardName], '1 ' + cardName))
        else:
            self.selectedDeckList.cards[index]['quantity'] += 1
            self.textCardsInSelectedDeck[index].text.str = str(self.selectedDeckList.cards[index]['quantity']) + ' ' + cardName
    
    def removeOneCard(self, cardName):
        index = self.findIndexDictionary('name', cardName)
        self.textCardsInSelectedDeck[index].text.str = str(self.selectedDeckList.cards[index]['quantity'] - 1) + ' ' + cardName
        self.selectedDeckList.cards[index]['quantity'] -= 1
        if self.selectedDeckList.cards[index]['quantity'] <= 0:
            del self.selectedDeckList.cards[index]
            self.textCardsInSelectedDeck[index].delete()
            self.textCardsInSelectedDeck.remove(self.textCardsInSelectedDeck[index])
            self.updateCardUiPosition()

    def updateCardUiPosition(self):
        for i, text in enumerate(self.textCardsInSelectedDeck):
            text.text.transform_component.position = calc_card_position(self.game, i + 2)