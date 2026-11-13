import pygame
from card_game.entities.entity import Entity
from card_game.core.constants import RED


class TargetHighlight(Entity):
    """Draws a red overlay over a card while it can be attacked.

    There is one highlight per card (like PlayCardRectangle and
    SelectedCardMarker) so it is always drawn right after its own card. A
    single shared highlight would be added to the game objects before the
    cards exist and every card image would paint over it.
    """

    def on_init(self, card) -> None:
        self.card = card
        self.outline_thickness = 5
        self.create_surface()

    def create_surface(self):
        width, height = self.card.transform_component.rect.size
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((*RED, 60))
        pygame.draw.rect(self.surface, RED, self.surface.get_rect(), self.outline_thickness)

    def draw(self):
        self.game.screen.blit(self.surface, self.card.transform_component.rect.topleft)

    def update(self):
        if self.card.is_attack_target():
            self.draw()
