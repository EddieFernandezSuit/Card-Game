from entities.entity import Entity
import pygame

class UIContainer(Entity):
    def on_init(self, position, padding=10, elements=None):
        self.position = pygame.Vector2(position)
        self.padding = padding
        self.elements = []
        if elements:
            self.add_elements(elements)

    def add_element(self, element):
        self.elements.append(element)
        self.update_positions()

    def add_elements(self, elements):
        self.elements.extend(elements)
        self.update_positions()

    def update_positions(self):
        current_y = self.position.y
        for element in self.elements:
            element.transform_component.position = pygame.Vector2(self.position.x, current_y)
            current_y += element.transform_component.height + self.padding

    def on_delete(self):
        for element in self.elements:
            element.delete()