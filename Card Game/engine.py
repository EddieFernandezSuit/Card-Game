import pygame
import sys

class Color:
    GREY = (150, 150, 150)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    PINK = (220, 20, 60)
    PURPLE = (138, 43, 226)
    ORANGE = (255, 165, 0)
    WHITE = (255, 255, 255)


class Game:
    def __init__(self, Width, height, start, update):
        pygame.init()
        self.width = Width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.myFont = pygame.font.SysFont("arial", 25)
        self.run = True
        self.gameStates = []
        self.state = None
        self.pause = 0
        self.pauseTimer = 0
        self.pauseTime = 60
        start(self)

        while self.run:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    sys.exit()
            self.clock.tick(60)
            if self.pause == 1:
                self.pauseTimer += 1
                if self.pauseTimer > self.pauseTime:
                    self.pause = 0
                    self.pauseTimer = 0

            if self.pause == 0:
                self.screen.fill(Color.GREY)
                update(self)
                pygame.display.update()



class GameState:
    def __init__(self, game, name):
        self.objects = []
        self.game = game
        game.gameStates.append(self)

