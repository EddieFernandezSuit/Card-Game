from entities.entity import Entity
from entities.DeckList import DeckList
from entities.ClickableText import ClickableText
from entities.DeckList import calculateCardPosition
from entities.DeckList import deckUi
from entities.TextHandler import TextHandler
import pygame

class DeckBox(Entity):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.deckLists = []
        self.textCardsInSelectedDeck = []
        self.AddDeckButton = ClickableText(game, pygame.Vector2(10, 10), self.addDeck, [], 'Add Deck', game.fonts['medium'])
        position = pygame.Vector2(deckUi['offset'], deckUi['offset'] + 5 * deckUi['yGap'])
        self.selectedDeckText = TextHandler(game, 'Deck 0', position, game.fonts['medium'])
        self.selectedDeckList = {}
    
    def changeDeck(self, deckList):
        for text in self.textCardsInSelectedDeck:
            text.delete()
        
        self.textCardsInSelectedDeck = []
        self.selectedDeckText.str = deckList.deckName
        self.selectedDeckList = deckList

        for j, card in enumerate(deckList.cards):
            i = j + 2
            self.textCardsInSelectedDeck.append(ClickableText(self.game, calculateCardPosition(self.game, i), self.removeOneCard, [card['name']], str(card['quantity']) + ' ' + card['name'], self.game.fonts['medium']))
        
    def addDeck(self):
        deckName = 'Deck ' + str(len(self.deckLists))
        deckList = DeckList(self.game, deckName)
        self.changeDeck(deckList)
        self.deckLists.append(self.selectedDeckList)
        self.AddDeckButton.textHandler.transform_component.position.y = 10 + len(self.deckLists) * 30
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
            self.textCardsInSelectedDeck.append(ClickableText(self.game, calculateCardPosition(self.game, len(self.selectedDeckList.cards) + 1), self.removeOneCard, [cardName], '1 ' + cardName, self.game.fonts['medium']))
        else:
            self.selectedDeckList.cards[index]['quantity'] += 1
            self.textCardsInSelectedDeck[index].textHandler.str = str(self.selectedDeckList.cards[index]['quantity']) + ' ' + cardName
    
    def removeOneCard(self, cardName):
        index = self.findIndexDictionary('name', cardName)
        self.textCardsInSelectedDeck[index].textHandler.str = str(self.selectedDeckList.cards[index]['quantity'] - 1) + ' ' + cardName
        self.selectedDeckList.cards[index]['quantity'] -= 1
        if self.selectedDeckList.cards[index]['quantity'] <= 0:
            del self.selectedDeckList.cards[index]
            self.textCardsInSelectedDeck[index].delete()
            self.textCardsInSelectedDeck.remove(self.textCardsInSelectedDeck[index])
            self.updateCardUiPosition()

    def updateCardUiPosition(self):
        for i, text in enumerate(self.textCardsInSelectedDeck):
            text.textHandler.transform_component.position = calculateCardPosition(self.game, i + 2)