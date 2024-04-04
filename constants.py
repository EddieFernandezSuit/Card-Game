import pygame

pygame.init()

FONT_SIZE_SMALL = 25
FONT_SIZE_MEDIUM = 40
FONT_SIZE_LARGE = 60

FONT_NAME_SERIF = "freesansbold"

FONTS = {
    'small': pygame.font.SysFont(FONT_NAME_SERIF, FONT_SIZE_SMALL),
    'medium': pygame.font.SysFont(FONT_NAME_SERIF, FONT_SIZE_MEDIUM),
    'large': pygame.font.SysFont(FONT_NAME_SERIF, FONT_SIZE_LARGE)
}
