from entities.entity import Entity
import pygame

class UIContainer(Entity):
    def on_init(self, position, padding=10, elements=None, isCenterX=False, isCenterY=False, isCenter=False):
        self.position = pygame.Vector2(position)
        self.padding = padding
        self.elements = []
        self.size = (0,0)
        self.isCenterX = isCenterX
        self.isCenterY = isCenterY
        if isCenter:
            self.isCenterX = self.isCenterY = True
        if elements:
            self.add_elements(elements)

    def add_element(self, element):
        self.size = (max(element.transform_component.width, self.size[0]), self.size[1] + element.transform_component.height + (self.padding if len(self.elements) > 0 else 0))
        self.elements.append(element)
        self.update_positions()

    def add_elements(self, elements):
        for element in elements:
            self.add_element(element)

    def update_position(self, position):
        self.position = position
        self.update_positions()

    def update_positions(self):
        current_y = self.position.y
        if self.isCenterY:
            current_y -= self.size[1]/2

        for element in self.elements:
            if element != self.elements[0]:
                current_y += element.transform_component.height + self.padding
            element.transform_component.position = pygame.Vector2(self.position.x, current_y)
            if self.isCenterX:
                element.transform_component.position.x -= (element.transform_component.width/2)

    def on_delete(self):
        for element in self.elements:
            element.delete()