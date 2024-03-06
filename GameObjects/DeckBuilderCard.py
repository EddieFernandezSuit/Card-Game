from GameObjects.GameObject import GameObject
from Handlers.TransformHandler import TransformHandler
from Handlers.ImageHandler import ImageHandler
from Handlers.TextHandler import TextHandler
from Handlers.ClickHandler import ClickHandler
import GameObjects.DeckList
import json
import pygame
import Colors

class DeckBuilderCard(GameObject):
    def __init__(self, game, cardName, position: tuple) -> None:
        super().__init__(game)
        cardData = json.load(open('cardData.json'))
        self.stats = cardData[cardName]
        self.cardName = cardName
        self.TransformHandler = TransformHandler(game, pygame.Vector2(position))
        self.imageHandler = ImageHandler('images/' + self.cardName.lower() + '.jpg', self.TransformHandler.position, game)
        self.rect = pygame.Rect(self.TransformHandler.position.x, self.TransformHandler.position.y, self.imageHandler.image.get_rect().width, self.imageHandler.image.get_rect().height)
        self.statsText = {}
        ncount = 0
        smallFont = game.fonts['small']
        textHeight = smallFont.size('A')[1]
        self.statsText['Name'] = TextHandler(game, self.cardName, self.TransformHandler.position, pygame.Vector2(5,5 + textHeight * ncount), smallFont)
        for key in self.stats:
            if self.stats[key] != 0 and key != 'Growth Type':
                ncount += 1
                self.statsText[key] = TextHandler(game, key + ' ' +  str(self.stats[key]), self.TransformHandler.position, pygame.Vector2(5,5 + textHeight * ncount), smallFont)
        self.statsText[self.stats['Growth Type']].color = Colors.LIGHTCYAN
        self.clickHandler = ClickHandler(self.rect, self.onClick, (game), game)
    
    def onClick(self, game):
        # deckCount = len(game.currentState['deckList'].cards)
        # position = GameObjects.DeckList.calculateCardPosition(self.game, deckCount)
        game.currentState['deckBox'].addCard(self.cardName)