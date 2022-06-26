import pygame
import Colors

class Game:
    def __init__(self, start, update, draw):
        pygame.init()
        self.SCREEN_WIDTH = 1600
        self.SCREEN_HEIGHT = 900
        self.fontSize = 35
        fontName = "freesansbold"
        self.font = pygame.font.SysFont(fontName, self.fontSize)
        self.resizeScreen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
        self.screen = self.resizeScreen.copy()
        # self.resizeScreen = pygame.display.set_mode((900,900), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
        start(self)
        while True:
            update(self)
            self.screen.fill(Colors.GREY)
            draw(self)
            pygame.display.update()
            self.resizeScreen.blit(pygame.transform.scale(self.screen, (self.resizeScreen.get_rect().size)), (0, 0))
