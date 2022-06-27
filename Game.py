import pygame
import Colors

class Game:
    def __init__(self, start, update, draw):
        pygame.init()
        self.SCREEN_WIDTH = 1600
        self.SCREEN_HEIGHT = 900
        fontSize = 35
        fontName = "freesansbold"
        self.font = pygame.font.SysFont(fontName, fontSize)
        self.resizeScreen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
        self.screen = self.resizeScreen.copy()
        self.gameObjects = []
        start(self)
        while True:
            self.screen.fill(Colors.GREY)
            for gameObject in self.gameObjects:
                gameObject.update()
            update(self)
            draw(self)
            pygame.display.update()
            self.resizeScreen.blit(pygame.transform.scale(self.screen, (self.resizeScreen.get_rect().size)), (0, 0))
