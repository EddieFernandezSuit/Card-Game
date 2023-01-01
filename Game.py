import pygame
import Colors

class Game:
    def __init__(self, start, update, draw):
        pygame.init()
        self.SCREEN_WIDTH = 1600
        self.SCREEN_HEIGHT = 900
        # self.font = pygame.font.SysFont("freesansbold", 40)
        # self.smallFont = pygame.font.SysFont("freesansbold", 30)
        # self.bigFont = pygame.font.SysFont("freesansbold", 60)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        # self.gameObjects = []
        self.states = {
            'menu': {'gameObjects': []},
            'play': {'gameObjects': []},
        }
        self.currentState = 'play'

        self.states[self.currentState]['bigFont'] = pygame.font.SysFont("freesansbold", 60)
        self.states[self.currentState]['smallFont'] = pygame.font.SysFont("freesansbold", 30)
        self.states[self.currentState]['font'] = pygame.font.SysFont("freesansbold", 40)
        FPS = 60
        fpsClock = pygame.time.Clock()
        start(self)
        while True:
            self.screen.fill(Colors.GREY)
            for gameObject in self.states[self.currentState]['gameObjects']:
                gameObject.update()
            update(self)
            draw(self)
            pygame.display.update()
            fpsClock.tick(FPS)
