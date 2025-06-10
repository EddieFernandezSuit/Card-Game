from entities.entity import Entity
from components.transform_component import TransformComponent
from components.image_component import ImageComponent
from entities.text import Text
from components.click_component import ClickComponent
from constants import *
import json
import pygame

class DeckBuilderCard(Entity):
    def on_init(self, cardName, position: tuple) -> None:
        cardData = json.load(open('cardData.json'))
        self.stats = cardData[cardName]
        self.cardName = cardName
        self.add_components(
            TransformComponent(self.game, position),
            ImageComponent(self.game, filePath='images/' + self.cardName.lower() + '.jpg', entity=self),
            ClickComponent(entity=self)
        )
        self.statsText = {}
        ncount = 0
        for key in self.stats:
            if key != 'Growth Type' and self.stats[key]:
                if key != 'Name':
                    self.statsText[key] = Text(self.game, key + ' ' +  str(self.stats[key]),font_size= 'small')
                else:
                    self.statsText[key] = Text(self.game, str(self.stats[key]),font_size= 'small')
                ncount += 1

        self.statsText[self.stats['Growth Type']].color = LIGHTCYAN

    def on_click(self):
        self.game.currentState['deckBox'].addCard(self.cardName)

    def update(self):
        ncount = 0
        textHeight = self.game.fonts['small'].size('A')[1]
        for key in self.statsText:
            self.statsText[key].transform_component.position = self.transform_component.position + pygame.Vector2(5,5 + textHeight * ncount)
            ncount += 1
            
    on_init.__annotations__ = {'cardName': str, 'position': 'Tuple[int, int]', 'return': None}
    