import pygame
from constants import *
import sys
from entities.text import Text

class Game:
    def __init__(self, start = lambda x: x, update= lambda x: x, draw = lambda x:x):
        self.__dict__.update(locals())
        pygame.init()
        self.SCREEN_WIDTH = 1500
        self.SCREEN_HEIGHT = 750
        self.fonts = {name: pygame.font.SysFont("freesansbold", size) for name, size in {'small': FONT_SIZE_SMALL, 'medium': FONT_SIZE_MEDIUM, 'large': FONT_SIZE_LARGE}.items()}
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.currentState = {}
        # self.states={'menu': None}
        self.key_actions = {}
        FPS = 120
        self.clock = pygame.time.Clock()
        start(self)
        fps_text = Text(self, 'FPS: 0', (self.SCREEN_WIDTH - 100, 10), 'small', WHITE)
        while True:
            self.handle_events()
            self.screen.fill(GREY)
            fps_text.str = f'FPS: {int(self.clock.get_fps())}'

            for gameObject in self.currentState['gameObjects']:
                gameObject.update()
           
            update(self)
            draw(self)

            pygame.display.update()
            self.clock.tick(FPS)

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

    def send(self, object):
        self.currentState['client'].send(object)
    
    def set_state(self, state_name):
        self.currentState = self.states[state_name]
        self.state = self.states[state_name]
        if not self.currentState.is_state_created:
            self.currentState.is_state_created = True
            self.currentState.create()

