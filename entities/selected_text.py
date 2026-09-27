import pygame
from entities.entity import Entity
from constants import BLACK, WHITE

SELECTED_SYMBOL = 'X'


class SelectedCardMarker(Entity):
    """Draws an X over a card while that card is the selected card.

    There is one marker per card (like PlayCardRectangle) so it is always
    drawn right after its own card. A single shared marker gets added to the
    game objects before any card exists, and since draw order is game object
    insertion order, every card image paints over it and hides it.
    """

    def on_init(self, card) -> None:
        self.card = card
        self.font = self.game.fonts['large']
        self.outline_offset = 2
        self.glyph = self.font.render(SELECTED_SYMBOL, 1, WHITE)
        self.glyph_outline = self.font.render(SELECTED_SYMBOL, 1, BLACK)

    def draw(self):
        glyph_rect = self.glyph.get_rect(center=self.card.transform_component.rect.center)
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        offset = self.outline_offset
        for position in offsets:
            self.game.screen.blit(self.glyph_outline, glyph_rect.move(position[0] * offset, position[1] * offset))
        self.game.screen.blit(self.glyph, glyph_rect)

    def update(self):
        if self.game.currentState['selectedCard'] is self.card:
            self.draw()
