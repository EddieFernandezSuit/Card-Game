
import pygame
from constants import *
from entities.entity import Entity
from entities.text import Text
from components.click_component import ClickComponent

class ClickableText(Entity):
    """
    A clickable text entity that changes color when hovered over.

    Args:
        game (Game): The game object.
        position (tuple): The position of the text.
        on_click (function): The function to call when the text is clicked.
        args (list): The arguments to pass to the on_click function.
        str (str): The text to display.
        font_size (str, optional): The size of the font. Defaults to 'medium'.

    Attributes:
        on_click (function): The function to call when the text is clicked.
        text (Text): The text entity.
        transform_component (TransformComponent): The transform component of the text entity.
        click_component (ClickComponent): The click component of the text entity.
    """
    def on_init(self, position=(0,0), on_click=lambda : (), args = [], str ='', font_size='medium'):
        self.on_click = on_click
        self.text = Text(self.game, str, position, font_size)
        self.transform_component = self.text.transform_component
        MENU_CLICK_FILENAME = 'sounds/menu_click.wav'
        MENU_CLICK_SOUND = pygame.mixer.Sound(MENU_CLICK_FILENAME)
        self.click_component = ClickComponent(args, self, sound=MENU_CLICK_SOUND)
        self.update()

    def update(self):
        mouse_position = pygame.mouse.get_pos()
        self.text.color = CYAN if self.transform_component.rect.collidepoint(pygame.Vector2(mouse_position)) else WHITE

    def on_delete(self):
        self.text.delete()
        self.click_component.delete()