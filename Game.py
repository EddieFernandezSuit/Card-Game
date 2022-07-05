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
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # self.screen = self.resizeScreen.copy()
        self.gameObjects = []
        
        FPS = 60
        fpsClock = pygame.time.Clock()
        start(self)
        while 1:
            self.screen.fill(Colors.GREY)
            for gameObject in self.gameObjects:
                gameObject.update()
            update(self)
            draw(self)
            pygame.display.update()
            # self.resizeScreen.blit(pygame.transform.scale(self.screen, (self.resizeScreen.get_rect().size)), (0, 0))
            fpsClock.tick(FPS)
