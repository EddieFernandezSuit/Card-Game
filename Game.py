import pygame
from constants import *
import sys
from entities.text import Text

class Game:
    def __init__(self, start, update, draw):
        self.__dict__.update(locals())
        pygame.init()
        self.SCREEN_WIDTH = 1800
        self.SCREEN_HEIGHT = 900
        self.fonts = {name: pygame.font.SysFont("freesansbold", size) for name, size in {'small': 25, 'medium': 40, 'large': 60}.items()}
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.key_actions = {}
        FPS = 120
        clock = pygame.time.Clock()
        start(self)
        fps_text = Text(self, 'FPS: 0', (self.SCREEN_WIDTH - 100, 10), 'small', WHITE)
        while True:
            self.handle_events()
            self.screen.fill(GREY)
            fps_text.str = f'FPS: {int(clock.get_fps())}'

            for gameObject in self.currentState['gameObjects']:
                gameObject.update()
           
            update(self)
            draw(self)

            pygame.display.update()
            clock.tick(FPS)

    def handle_events(self):
        self.events = pygame.event.get()
        key_actions = self.key_actions
        for event in self.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in key_actions:
                    key_actions[event.key]()
