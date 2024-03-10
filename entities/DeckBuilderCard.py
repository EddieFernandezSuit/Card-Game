from entities.entity import Entity
from components.transform_component import TransformComponent
from components.image_component import ImageComponent
from entities.TextHandler import TextHandler
from components.click_component import ClickComponent
import json
import pygame
import Colors

class DeckBuilderCard(Entity):
    def __init__(self, game, cardName, position: tuple) -> None:
        super().__init__(game)
        cardData = json.load(open('cardData.json'))
        self.stats = cardData[cardName]
        self.cardName = cardName
        self.transform_component = TransformComponent(game, pygame.Vector2(position))
        self.imageHandler = ImageComponent('images/' + self.cardName.lower() + '.jpg', self)
        self.rect = pygame.Rect(self.transform_component.position.x, self.transform_component.position.y, self.imageHandler.image.get_rect().width, self.imageHandler.image.get_rect().height)
        self.statsText = {}
        ncount = 0
        smallFont = game.fonts['small']
        textHeight = smallFont.size('A')[1]
        self.statsText['Name'] = TextHandler(game, self.cardName, self.transform_component.position, pygame.Vector2(5,5 + textHeight * ncount), smallFont)
        for key in self.stats:
            if self.stats[key] != 0 and key != 'Growth Type':
                ncount += 1
                self.statsText[key] = TextHandler(game, key + ' ' +  str(self.stats[key]), self.transform_component.position, pygame.Vector2(5,5 + textHeight * ncount), smallFont)
        self.statsText[self.stats['Growth Type']].color = Colors.LIGHTCYAN
        self.clickHandler = ClickComponent((), self)
    
    def on_click(self):
        # deckCount = len(game.currentState['deckList'].cards)
        # position = entities.DeckList.calculateCardPosition(self.game, deckCount)
        self.game.currentState['deckBox'].addCard(self.cardName)