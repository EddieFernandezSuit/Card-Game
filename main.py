import pygame
import sys
import os
import Colors
from asyncio.windows_events import NULL
from Handlers.ImageHandler import ImageHandler
from GameObjects.PassTurnButton import PassTurnButton
from GameObjects.Player import Player
from Game import Game


def drawOutlineText(game,str,x,y):
    img = game.font.render(str, 1, Colors.BLACK)
    game.screen.blit(img, (x + 1, y + 1))
    game.screen.blit(img, (x - 1, y + 1))
    game.screen.blit(img, (x + 1, y - 1))
    game.screen.blit(img, (x - 1, y - 1))
    game.screen.blit(game.font.render(str, 1, Colors.WHITE), (x, y))

def start(game):
    game.background = ImageHandler('Images/background.jpg', pygame.Vector2(0,0), game)
    game.passTurnButton = PassTurnButton(game)
    game.turn = 0
    game.turnRectangle = pygame.Rect(150, 0, 1150, 450)
    game.selectedCard = NULL
    game.players = [Player(game,0), Player(game,1)]

def update(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.passTurnButton.onClick(game)

def draw(game):
    if game.selectedCard != NULL:
        drawOutlineText(game,'X', game.selectedCard.position.x + 100, game.selectedCard.position.y +100)
    pygame.draw.rect(game.screen, Colors.BLACK, game.turnRectangle, 3)

Game(start, update, draw)
