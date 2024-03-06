from GameObjects.GameObject import GameObject
from GameObjects.DeckList import DeckList
from GameObjects.ClickableText import ClickableText
from GameObjects.DeckList import calculateCardPosition
from GameObjects.DeckList import deckUi
from Handlers.TextHandler import TextHandler
import pygame

class DeckBox(GameObject):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.deckLists = []
        self.textCardsInSelectedDeck = []
        self.AddDeckButton = ClickableText(game, pygame.Vector2(10, 10), self.addDeck, ('deck'), 'Add Deck', game.fonts['medium'])
        position = pygame.Vector2(deckUi['offset'], deckUi['offset'] + 4 * deckUi['yGap'])
        self.selectedDeckText = TextHandler(game, 'Deck 0', position, pygame.Vector2(0,0), game.fonts['medium'])
        self.selectedDeckList = {}

    def placeHolder():
        pass
    
    def changeDeck(self, deckList):
        for text in self.textCardsInSelectedDeck:
            text.delete()
        
        self.textCardsInSelectedDeck = []
        self.selectedDeckText.str = deckList.deckName
        self.selectedDeckList = deckList
        i = 1
        for card in deckList.cards:
            self.textCardsInSelectedDeck.append(ClickableText(self.game, calculateCardPosition(self.game, i), self.removeOneCard, (card['name']), str(card['quantity']) + ' ' + card['name'], self.game.fonts['medium']))
            i += 1
        
    def addDeck(self, game):
        deckName = 'Deck ' + str(len(self.deckLists))
        deckList = DeckList(self.game, deckName)
        self.changeDeck(deckList)
        self.deckLists.append(self.selectedDeckList)
        self.AddDeckButton.transformHandler.position.y = 10 + len(self.deckLists) * 30
        self.selectedDeckText.basePosition.y = 10 + (len(self.deckLists) + 2) * 30
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
            self.textCardsInSelectedDeck.append(ClickableText(self.game, calculateCardPosition(self.game, len(self.selectedDeckList.cards)), self.removeOneCard, (cardName), '1 ' + cardName, self.game.fonts['medium']))
        else:
            self.selectedDeckList.cards[index]['quantity'] += 1
            self.textCardsInSelectedDeck[index].textHandler.str = str(self.selectedDeckList.cards[index]['quantity']) + ' ' + cardName
    
    def removeOneCard(self, cardName):
        index = self.findIndexDictionary('name', cardName)
        self.textCardsInSelectedDeck[index].textHandler.str = str(self.selectedDeckList.cards[index]['quantity'] - 1) + ' ' + cardName
        self.selectedDeckList.cards[index]['quantity'] -= 1
        if self.selectedDeckList.cards[index]['quantity'] <= 0:
            self.textCardsInSelectedDeck[index].delete()
            del self.textCardsInSelectedDeck[index]
            del self.selectedDeckList.cards[index]
            self.updateCardUiPosition()

    def updateCardUiPosition(self):
        for i, text in enumerate(self.textCardsInSelectedDeck):
            newPos = calculateCardPosition(self.game, i + 1)
            text.transformHandler.position.x = newPos.x
            text.transformHandler.position.y = newPos.y