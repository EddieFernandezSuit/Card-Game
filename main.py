import pygame
import sys
import os
import Colors
from asyncio.windows_events import NULL
from Handlers.ImageHandler import ImageHandler
from GameObjects.PassTurnButton import PassTurnButton
from GameObjects.Player import Player
from GameObjects.ClickableText import ClickableText
from GameObjects.DeckBuilderCard import DeckBuilderCard
from GameObjects.DeckBox import DeckBox
from Game import Game
import json

def drawOutlineText(game, str, x, y):
    img = game.fonts["medium"].render(str, 1, Colors.BLACK)
    game.screen.blit(img, (x + 1, y + 1))
    game.screen.blit(img, (x - 1, y + 1))
    game.screen.blit(img, (x + 1, y - 1))
    game.screen.blit(img, (x - 1, y - 1))
    game.screen.blit(game.fonts["medium"].render(str, 1, Colors.WHITE), (x, y))

def clickPlay(game):
    game.currentState = game.states['play']
    game.currentState['background'] = ImageHandler('Images/background.jpg', pygame.Vector2(0,0), game)
    game.currentState['passTurnButton'] = PassTurnButton(game)
    game.currentState['turn'] = 0
    game.currentState['turnRectangle'] = pygame.Rect(150, 0, 1150, 450)
    game.currentState['selectedCard'] = NULL
    game.currentState['players'] = [Player(game,0), Player(game,1)]
    game.currentState['arrowFlies'] = 0

def to_matrix(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def createDeckBuilderState(game):
    game.currentState = game.states['buildDeck']
    game.currentState['background'] = ImageHandler('Images/background.jpg', pygame.Vector2(0,0), game)
    cardsJson = json.load(open('cardData.json'))
    collumns = 3
    cardsInMatrix = to_matrix(list(cardsJson.keys()), collumns)

    for i in range(len(cardsInMatrix)):
        for j in range(len(cardsInMatrix[i])):
            cardSize = 200
            game.currentState['cardsToAdd'].append(DeckBuilderCard(game, cardsInMatrix[i][j], (400 + j * (cardSize + 10), 10 + i * (cardSize + 10))))

    game.currentState['deckBox'] = DeckBox(game)

    deckBoxData = {}
    with open('DeckBox.json') as deckboxFile:
        deckBoxData = json.load(deckboxFile)

    for key in deckBoxData:
        deckList = game.currentState['deckBox'].addDeck(key)
        for card in deckBoxData[key]:
            deckList.cards.append(card)

    game.currentState['save and exit'] = ClickableText(game, pygame.Vector2(10, game.SCREEN_HEIGHT - game.fonts['medium'].size('A')[1] - 10), saveAndExit, (game), 'Save and Exit', game.fonts['medium'])
    game.currentState = game.states['menu']

def saveAndExit(game):
    deckBox = {}
    for deckList in game.currentState['deckBox'].deckLists:
        deckBox[deckList.deckName] = deckList.cards
    
    with open('DeckBox.json', 'w') as db:
        json.dump(deckBox, db) 
            
    game.currentState = game.states['menu']

def changeToDeckBuilder(game):
    game.currentState = game.states['buildDeck']



def start(game):
    game.states = {
        'menu': {
            'stateName': 'menu',
            'gameObjects': []
        },
        'play': {
            'stateName': 'play',
            'gameObjects': []
        },
        'buildDeck': {
            'stateName': 'buildDeck',
            'gameObjects': [],
            'cardsToAdd': []
        },
    }
    game.currentState = game.states['menu']
    game.currentState['background'] = ImageHandler('Images/background.jpg', pygame.Vector2(0,0), game)
    game.currentState['MenuOptions'] = [
        ClickableText(game, pygame.Vector2(100, 100), clickPlay, (game), 'Play', game.fonts['medium']),
        ClickableText(game, pygame.Vector2(100, 150), changeToDeckBuilder, (game), 'Build Deck', game.fonts['medium']),
    ]

    createDeckBuilderState(game)

def update(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # game.passTurnButton.onClick(game)
                game.currentState['passTurnButton'].onClick(game)

def draw(game):
    if game.currentState['stateName'] == 'play':
        if game.currentState['selectedCard'] != NULL:
            drawOutlineText(game,'X', game.currentState['selectedCard'].position.x + 100, game.currentState['selectedCard'].position.y +100)
        pygame.draw.rect(game.screen, Colors.BLACK, game.currentState['turnRectangle'], 3)

Game(start, update, draw)


