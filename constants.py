import pygame

pygame.init()

FONT_SIZE_SMALL = 30
FONT_SIZE_MEDIUM = 40
FONT_SIZE_LARGE = 60
FONT_NAME_SERIF = "freesansbold"

FONTS = {
    'small': pygame.font.SysFont(FONT_NAME_SERIF, FONT_SIZE_SMALL),
    'medium': pygame.font.SysFont(FONT_NAME_SERIF, FONT_SIZE_MEDIUM),
    'large': pygame.font.SysFont(FONT_NAME_SERIF, FONT_SIZE_LARGE)
}

GREY = (150, 150, 150)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 100, 100)
GREEN = (0, 255, 0)
LIGHT_GREEN = (100, 255, 100)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PINK = (220, 20, 60)
PURPLE = (138, 43, 226)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
LIGHTCYAN = (180,255,255)

CARD_SIZE = 160