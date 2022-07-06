from asyncio.windows_events import NULL
import pygame
import sys
import Colors
from Game import Game
from PassTurnButton import PassTurnButton
from Player import Player

def drawOutlineText(game,str,x,y,):
    img = game.font.render(str, 1, Colors.BLACK)
    game.screen.blit(img, (x + 1, y + 1))
    game.screen.blit(img, (x - 1, y + 1))
    game.screen.blit(img, (x + 1, y - 1))
    game.screen.blit(img, (x - 1, y - 1))
    game.screen.blit(game.font.render(str, 1, Colors.WHITE), (x, y))

def cardPositionX(i):
    return 5 + 205 * (i + 1)

def start(game):
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
