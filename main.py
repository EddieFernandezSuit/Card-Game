import pygame
import sys
import Colors
import json
from asyncio.windows_events import NULL
from entities.PassTurnButton import PassTurnButton
from entities.Player import Player
from entities.ClickableText import ClickableText
from entities.DeckBuilderCard import DeckBuilderCard
from entities.DeckBox import DeckBox
from entities.TextHandler import TextHandler
from entities.background import Background
from Game import Game


def draw_outline_text(game, str, x, y):
    text_outline_surface = game.fonts["medium"].render(str, 1, Colors.BLACK)
    text_surface = game.fonts["medium"].render(str, 1, Colors.WHITE)

    offsets = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    for offset_x, offset_y in offsets:
        game.screen.blit(text_outline_surface, (x + offset_x, y + offset_y))
    
    game.screen.blit(text_surface, (x, y))

def click_play(game):
    game.currentState = game.states['play']

    Background(game=game)

    state = {
        'passTurnButton': PassTurnButton(game),
        'turn': 0,
        'turnRectangle': pygame.Rect(150, 0, 1150, 450),
        'selectedCard': NULL,
        'players': [Player(game,0), Player(game,1)],
        'arrowFlies': 0,
        'select_text': TextHandler(game, 'X', pygame.Vector2(100, 100), game.fonts['big'])
    }

    game.currentState.update(state)

def to_matrix(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def json_to_dictionary(json_filename):
    dict = {}
    with open(json_filename) as file:
        dict = json.load(file)
    return dict

def create_deck_builder_state(game):
    game.currentState = game.states['buildDeck']
    
    Background(game)
    game.currentState['deckBox'] = DeckBox(game)
    
    card_data = json_to_dictionary('cardData.json')
    deck_box_data = json_to_dictionary('DeckBox.json')

    collumns = 3
    cards_in_matrix = to_matrix(list(card_data.keys()), collumns)

    for i, _ in enumerate(cards_in_matrix):
        for j, _ in enumerate(cards_in_matrix[i]):
            card_size = 200
            card_spacing = 10
            game.currentState['cardsToAdd'].append(DeckBuilderCard(game, cards_in_matrix[i][j], (400 + j * (card_size + card_spacing), card_spacing + i * (card_size + card_spacing))))

    for key in deck_box_data:
        deckList = game.currentState['deckBox'].addDeck()
        for card in deck_box_data[key]:
            deckList.cards.append(card)

    game.currentState['save and exit'] = ClickableText(game, pygame.Vector2(10, game.SCREEN_HEIGHT - game.fonts['medium'].size('A')[1] - 10), save_and_exit, (game), 'Save and Exit', game.fonts['medium'])
    game.currentState = game.states['menu']

def save_and_exit(game):
    deckBox = {}
    for deckList in game.currentState['deckBox'].deckLists:
        deckBox[deckList.deckName] = deckList.cards
    
    with open('DeckBox.json', 'w') as db:
        json.dump(deckBox, db) 
            
    game.currentState = game.states['menu']

def change_to_deck_builder(game):
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
    
    Background(game=game)
    game.currentState['MenuOptions'] = [
        ClickableText(game, pygame.Vector2(100, 100), click_play, [game], 'Play', game.fonts['medium']),
        ClickableText(game, pygame.Vector2(100, 150), change_to_deck_builder, [game], 'Build Deck', game.fonts['medium']),
    ]

    create_deck_builder_state(game)

def update(game):
    for gameObject in game.currentState['gameObjects']:
        gameObject.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.currentState['passTurnButton'].onClick(game)

def draw(game):
    if game.currentState['stateName'] == 'play':
        if game.currentState['selectedCard'] != NULL:
            game.currentState['select_text'].transform_component.position = game.currentState['selectedCard'].transform_component.position + (100,100)

        game.currentState['select_text'].visible = game.currentState['selectedCard'] != NULL
        pygame.draw.rect(game.screen, Colors.BLACK, game.currentState['turnRectangle'], 3)

Game(start, update, draw)


