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
        if deckList is not None:
            self.selectedDeckText.str = deckList.deckName
            self.selectedDeckList = deckList

            for j, card in enumerate(deckList.cards):
                i = j + 2
                self.textCardsInSelectedDeck.append(ClickableText(self.game, calc_card_position(self.game, i), self.removeOneCard, [card['name']], str(card['quantity']) + ' ' + card['name']))
        else:
            self.selectedDeckText.str = ''
            self.selectedDeckList = None

    def addDeck(self):
        deckName = 'Deck ' + str(len(self.deckLists))
        deckList = DeckList(self.game, deckName)
        self.changeDeck(deckList)
        self.deckLists.append(self.selectedDeckList)
        self.updateDeckUiPosition()
        self.updateCardUiPosition()
        return deckList
    
    def findIndexDictionary(self, key, value):
        for i, dict in enumerate(self.selectedDeckList.cards):
            if dict[key] == value:
                return i
        return -1

    def updateCardQuantity(self, index, quantity_change, card_name):
        self.selectedDeckList.cards[index]['quantity'] += quantity_change
        self.textCardsInSelectedDeck[index].text.str = str(self.selectedDeckList.cards[index]['quantity']) + ' ' + card_name

    def addCard(self, card_name):
        index = self.findIndexDictionary('name', card_name)
        if index == -1:
            self.selectedDeckList.cards.append({'quantity': 1, 'name': card_name})
            self.textCardsInSelectedDeck.append(ClickableText(self.game, calc_card_position(self.game, len(self.selectedDeckList.cards) + 1), self.removeOneCard, [card_name], '1 ' + card_name))
        else:
            self.updateCardQuantity(index, 1, card_name)

    def removeOneCard(self, cardName):
        index = self.findIndexDictionary('name', cardName)
        self.updateCardQuantity(index, -1, cardName)
        if self.selectedDeckList.cards[index]['quantity'] <= 0:
            del self.selectedDeckList.cards[index]
            self.textCardsInSelectedDeck[index].delete()
            self.textCardsInSelectedDeck.remove(self.textCardsInSelectedDeck[index])
            self.updateCardUiPosition()

    def updateCardUiPosition(self):
        for i, text in enumerate(self.textCardsInSelectedDeck):
            text.text.transform_component.position = calc_card_position(self.game, i + 2)

    def deleteDeck(self, deckList):
        if self.selectedDeckList == deckList:
            self.changeDeck(None)
        self.deckLists.remove(deckList)
        self.updateDeckUiPosition()

    def updateDeckUiPosition(self):
        for i, deck in enumerate(self.deckLists):
            deck.nameText.text.transform_component.position.y = deckUi['offset'] + i * deckUi['yGap']
            deck.deleteButton.text.transform_component.position.y = deckUi['offset'] + i * deckUi['yGap']
        self.AddDeckButton.text.transform_component.position.y = 10 + len(self.deckLists) * 30
        self.selectedDeckText.transform_component.position.y = 10 + (len(self.deckLists) + 3) * 30