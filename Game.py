import pygame
import Colors
import sys

class Game:
    def __init__(self, start, update, draw):
        pygame.init()
        self.start = start
        self.update = update
        self.draw = draw
        self.SCREEN_WIDTH = 1600
        self.SCREEN_HEIGHT = 900
        self.fonts = {name: pygame.font.SysFont("freesansbold", size) for name, size in {'small': 25, 'medium': 40, 'large': 60}.items()}
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        FPS = 60
        fpsClock = pygame.time.Clock()
        start(self)
        while True:
            self.screen.fill(Colors.GREY)
            update(self)
            draw(self)
            pygame.display.update()
            fpsClock.tick(FPS)

    def handle_events(self, key_actions):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in key_actions:
                    key_actions[event.key]()
