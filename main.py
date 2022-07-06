from asyncio.windows_events import NULL
import pygame
import sys
import Colors
from Game import Game
from EmptyZone import EmptyZone
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
    game.phase = 'play'
    game.passTurnButton = PassTurnButton(game)
    game.turn = 0
    game.turnRectangle = pygame.Rect(150, 0, 1150, 450)
    game.selectedCard = NULL
    fieldPositionY = [210, game.SCREEN_HEIGHT - 410]
    game.emptyZones = []

    for x in range(2):
        for y in range(5):
            game.emptyZones.append(EmptyZone(pygame.Vector2(cardPositionX(y), fieldPositionY[x]), x, game))

    game.players = [Player(game,0), Player(game,1)]

def update(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.passTurnButton.onClick(game)
    
    # if game.selectedCard != NULL:
    #     game.selectedCard.position.x = pygame.mouse.get_pos()[0]
    #     game.selectedCard.position.y = pygame.mouse.get_pos()[1]

def draw(game):
    if game.selectedCard != NULL:
        drawOutlineText(game,'X', game.selectedCard.position.x + 100, game.selectedCard.position.y +100)

    pygame.draw.rect(game.screen, Colors.BLACK, game.turnRectangle, 3)

Game(start, update, draw)
