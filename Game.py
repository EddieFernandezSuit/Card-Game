import pygame
import Colors

class Game:
    def __init__(self, start, update, draw):
        pygame.init()
        self.start = start
        self.update = update
        self.draw = draw
        self.SCREEN_WIDTH = 1600
        self.SCREEN_HEIGHT = 900
        self.fonts = {
            'small': pygame.font.SysFont("freesansbold", 25),
            'medium': pygame.font.SysFont("freesansbold", 40),
            "big": pygame.font.SysFont("freesansbold", 60)
        }
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        FPS = 60
        fpsClock = pygame.time.Clock()
        start(self)
        while True:
            self.screen.fill(Colors.GREY)
            for gameObject in self.currentState['gameObjects']:
                gameObject.update()
            update(self)
            draw(self)
            pygame.display.update()
            fpsClock.tick(FPS)
