import pygame
from entities.entity import Entity

class ClickComponent(Entity):
    def __init__(self, args=[], entity=None, sound=None):
        super().__init__(entity.game)
        self.lastClick = 0
        self.args = args
        self.entity = entity
        self.sound = sound
    
    def update(self):
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 is the left mouse button
                if self.entity.transform_component.rect.collidepoint(event.pos):
                    # MENU_CLICK_FILENAME = 'sounds/menu_click.wav'
                    # MENU_CLICK_SOUND = pygame.mixer.Sound(MENU_CLICK_FILENAME)
                    # MENU_CLICK_SOUND.play()
                    if self.sound:
                        self.sound.play()
                    self.entity.on_click(*self.args)
