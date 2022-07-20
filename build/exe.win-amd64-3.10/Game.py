import pygame
import Colors

class Game:
    def __init__(self, start, update, draw):
        pygame.init()
        self.SCREEN_WIDTH = 1600
        self.SCREEN_HEIGHT = 900
        self.font = pygame.font.SysFont("freesansbold", 40)
        self.smallFont = pygame.font.SysFont("freesansbold", 30)
        self.bigFont = pygame.font.SysFont("freesansbold", 60)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # self.screen = self.resizeScreen.copy()
        self.gameObjects = []
        self.start = start
        self.update = update
        self.draw = draw        
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
