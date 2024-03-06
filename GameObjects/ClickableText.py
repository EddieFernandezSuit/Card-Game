
import pygame
from GameObjects.GameObject import GameObject
from Handlers.TransformHandler import TransformHandler
from Handlers.TextHandler import TextHandler
from Handlers.ClickHandler import ClickHandler
import Colors

class ClickableText(GameObject):
    def __init__(self, game, position, onClick, args, str, font) -> None:
        super().__init__(game)
        self.transformHandler = TransformHandler(game, pygame.Vector2(position))
        self.textHandler = TextHandler(game, str, self.transformHandler.position, pygame.Vector2(0,0), font)
        self.clickHandler = ClickHandler(self.textHandler.rect, onClick, args, game)
    
    def update(self):
        super().update()
        mousePosition = pygame.mouse.get_pos()
        if self.textHandler.rect.collidepoint(pygame.Vector2(mousePosition)):
            self.textHandler.color = Colors.CYAN
        else:
            self.textHandler.color = Colors.WHITE

    def delete(self):
        self.transformHandler.delete()
        self.textHandler.delete()
        self.clickHandler.delete()
        return super().delete()

