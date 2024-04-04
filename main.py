import pygame
import Colors
import json
from constants import FONTS
from entities.pass_turn_button import PassTurnButton
from entities.deck_builder_card import DeckBuilderCard
from entities.player import Player
from entities.clickable_text import ClickableText
from entities.deck_box import DeckBox
from entities.text import Text
from entities.background import Background
from Game import Game

def click_play(game):
    game.currentState = game.states['play']
    Background(game=game)

    state = {
        'passTurnButton': PassTurnButton(game),
        'turn': 0,
        'turnRectangle': pygame.Rect(150, 0, 1150, 450),
        'selectedCard': None,
        'players': [Player(game,0), Player(game,1)],
        'arrowFlies': 0,
        'select_text': Text(game, 'X', pygame.Vector2(100, 100), font_size='large')
    }

    pygame.mixer.Sound('sounds/background_music.mp3').play(-1)

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

    card_size = 200
    card_spacing = 10
    
    card_offset = card_size + card_spacing
    for i, row in enumerate(cards_in_matrix):
        for j, card in enumerate(row):
            game.currentState['cardsToAdd'].append(DeckBuilderCard(game, card, (400 + j * card_offset, card_spacing + i * card_offset)))
            
    for key in deck_box_data:
        deckList = game.currentState['deckBox'].addDeck()
        for card in deck_box_data[key]:
            deckList.cards.append(card)

    game.currentState['save and exit'] = ClickableText(game, pygame.Vector2(10, game.SCREEN_HEIGHT - FONTS['large'].size('A')[1] - 10), save_and_exit, [game], 'Save and Exit')
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
        ClickableText(game, pygame.Vector2(100, 100), click_play, [game], 'Play'),
        ClickableText(game, pygame.Vector2(100, 150), change_to_deck_builder, [game], 'Build Deck'),
    ]

    create_deck_builder_state(game)

def update(game):
    for gameObject in game.currentState['gameObjects']:
        gameObject.update()

    key_actions = {
        pygame.K_SPACE: lambda: game.currentState['passTurnButton'].on_click()
    }

    game.handle_events(key_actions)

def draw(game):
    if game.currentState['stateName'] == 'play':
        is_card_selected = game.currentState['selectedCard'] != None
        if is_card_selected:
            game.currentState['select_text'].transform_component.position = pygame.Vector2(game.currentState['selectedCard'].transform_component.rect.center)

        game.currentState['select_text'].visible = is_card_selected
        pygame.draw.rect(game.screen, Colors.BLACK, game.currentState['turnRectangle'], 3)

GAME = Game(start, update, draw)


