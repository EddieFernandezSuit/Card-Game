from entities.deck_builder_card import DeckBuilderCard
from entities.pass_turn_button import PassTurnButton
from entities.clickable_text import ClickableText
from entities.selected_text import TextSelector
from entities.ui_container import UIContainer
from entities.background import Background
from entities.deck_box import DeckBox
from entities.player import Player
from constants import *
from network import Client
from network import send
from Game import Game
import pygame
import json
import time

def click_play(game):
    game.currentState = game.states['play']
    Background(game=game)

    def update_game_state(client_state):
        if 'deck' in client_state:
            if 'players' in game.currentState:
                print('players', len(game.currentState['players']))
            if 'players' not in game.currentState or len(game.currentState['players']) == 1:
                print('here yes')
                game.currentState['new_player_deck'] = client_state['deck']
                game.currentState['create_new_player'] = True
                print(game.currentState['new_player_deck'])
                print(game.currentState['create_new_player'])

    game.currentState['client'] = Client(update_game_state)
    game.currentState['client'].send({})

    while game.currentState['client'].is_setup_complete() == False:
        pass

    state = {
        'passTurnButton': PassTurnButton(game),
        'turn': 0,
        'turnRectangle': pygame.Rect(150, 0, 1150, 450),
        'selectedCard': None,
        'players': [Player(game,0)],
        'arrowFlies': 0,
        'select_text': TextSelector(game),
        'background_music': pygame.mixer.Sound('sounds/background_music.mp3').play(-1),
        # 'create_new_player': False,
        # 'new_player_deck': None
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

    card_size = 200
    card_spacing = 10
    card_offset = card_size + card_spacing

    for i, row in enumerate(cards_in_matrix):
        for j, card in enumerate(row):
            deck_builder_card = DeckBuilderCard(game, card, (400 + j * card_offset, card_spacing + i * card_offset))
            game.currentState['cardsToAdd'].append(deck_builder_card)
            
    for key, deck_cards in deck_box_data.items():
        deck_list = game.currentState['deckBox'].addDeck()
        deck_list.cards.extend(deck_cards)

    game.currentState['save and exit'] = ClickableText(game, pygame.Vector2(10, game.SCREEN_HEIGHT - FONTS['large'].size('A')[1] - 10), save_and_exit, [game], 'Save and Exit')
    game.currentState = game.states['menu']

def save_and_exit(game):
    deckBox = {deckList.deckName: deckList.cards for deckList in game.currentState['deckBox'].deckLists}
    
    with open('DeckBox.json', 'w') as db:
        json.dump(deckBox, db) 
            
    game.currentState = game.states['menu']

def change_to_deck_builder(game):
    game.currentState = game.states['buildDeck']

def start(game):
    game.key_actions = {
        pygame.K_SPACE: lambda: game.currentState.get('passTurnButton', None) and game.currentState['passTurnButton'].on_click()
    }

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

    # game.currentState['MenuOptions'] = [
    #     ClickableText(game, pygame.Vector2(100, 100), click_play, [game], 'Play'),
    #     ClickableText(game, pygame.Vector2(100, 150), change_to_deck_builder, [game], 'Build Deck'),
    # ]

    game.ui_container = UIContainer(game, (100, 100), elements=[
        ClickableText(game, on_click=click_play, args=[game], str='Play'),
        ClickableText(game, on_click=change_to_deck_builder, args=[game], str='Build Deck'),
    ])

    create_deck_builder_state(game)

def update(game):
    if 'create_new_player' in game.currentState:
        print(game.currentState['create_new_player'])
    if 'create_new_player' in game.currentState and game.currentState['create_new_player']:
        game.currentState['players'].append(Player(game, 1, game.currentState['new_player_deck']))
        del game.currentState['create_new_player']
        del game.currentState['new_player_deck']


def draw(game):
    if game.currentState['stateName'] == 'play':
        pygame.draw.rect(game.screen, BLACK, game.currentState['turnRectangle'], 3)

GAME = Game(start, update, draw)