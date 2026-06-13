from constants import *
import pygame
from entities.entity import Entity
from components.transform_component import TransformComponent
from components.image_component import ImageComponent

class Text(Entity):
    """
    def on_init(self, str='', position=(0,0), font_size='medium', color=WHITE) -> None:
    """
    def on_init(self, str='', position=(0,0), font_size='medium', color=WHITE) -> None:
        self.__dict__.update(locals())
        self.visible = True
        self.font = self.game.fonts[font_size]
        font_surface = self.font.render(self.str, 1, self.color)
        width, height = self.font.size(self.str)
        self.width = width
        self.height = height
        self.add_components(TransformComponent(self.game, position, width=width, height=height), [ImageComponent(self.game, image=font_surface, entity=self) for _ in range(5)])

    def update(self):
        # Avoid re-rendering text every frame (font.render is expensive).
        # Only re-render when the text or color changes.
        if not getattr(self, "_last_render_key", None):
            self._last_render_key = object()

        current_key = (self.str, self.color, self.visible)
        if self.visible and current_key != self._last_render_key:
            positions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, 0)]

            for index, position in enumerate(positions):
                color = self.color if index == 4 else BLACK
                self.image_components[index].position_offset = position
                self.image_components[index].image = self.font.render(self.str, 1, color)

            self.transform_component.rect.size = self.font.size(self.str)

        # Toggle visibility for the underlying image components.
        for image_component in self.image_components:
            image_component.visible = self.visible

        self._last_render_key = current_key

    