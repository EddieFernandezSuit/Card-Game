from entities.deck_builder_card import DeckBuilderCard
from entities.pass_turn_button import PassTurnButton
from entities.clickable_text import ClickableText
from entities.selected_text import TextSelector
from entities.ui_container import UIContainer
from entities.background import Background
from entities.deck_box import DeckBox
from entities.player import Player
from particle_manager import ParticleManager
from thread_manager import ThreadManager
from entities.text import Text
from game_state import GameState
from constants import *
from network import Client
from Game import Game
import pygame
import json
import numpy as np


def get_opponent_player_num(game):
    return game.currentState['client'].client_id == 0
    
def get_opponent(game):
    opponent_num = get_opponent_player_num(game)
    return game.currentState['players'][opponent_num]

def click_play(game):
    game.currentState = game.states['play']
    if 'client' in game.states['connect']:
        game.currentState['client'] = game.states['connect'].client
    game.get_opponent = get_opponent

    def update_game_state(msg_obj):
        print('msg', msg_obj)
        if 'deck' in msg_obj and ('players' not in game.currentState ):
                def create_player(deck):
                    game.currentState['players'].append(Player(game, game.currentState['client'].client_id == 0, deck))
                    if game.currentState['client'].client_id == 1:
                        game.currentState['players'].reverse()
                game.thread_manager.do(create_player, msg_obj['deck'])
        
        if 'pass' in msg_obj:
            game.currentState['passTurnButton'].pass_turn()
        
        if 'play' in msg_obj:
            card_name = msg_obj['play']
            opponent = get_opponent(game)
            card = opponent.get_card_in_hand(card_name)
            card.play()

        if 'attacker' in msg_obj:
            attacking_player_num = msg_obj['attacker']['player_num']
            defending_player_num = attacking_player_num == 0

            attacking_card_field_id = msg_obj['attacker']['field_id']
            defending_card_field_id = msg_obj['defender']['field_id']
            print(defending_card_field_id, 'defending card field id')

            attacker = game.currentState['players'][attacking_player_num].field[attacking_card_field_id]
            # if not attacking player
            if defending_card_field_id != 'player':
                target = game.currentState['players'][defending_player_num].field[defending_card_field_id]
            else:
                target = game.currentState['players'][defending_player_num]
            
            game.thread_manager.do(lambda attacker, target: attacker.attack(target), attacker, target)
    
    if 'client' in game.states['connect']:
        game.currentState['client'].update_game_state = update_game_state
    
    state = {
        'background': Background(game=game),
        'turn': 0,
        'passTurnButton': PassTurnButton(game),
        'selectedCard': None,
        'players': [Player(game,game.currentState['client'].client_id)],
        'arrowFlies': 0,
        'select_text': TextSelector(game),
        'background_music': pygame.mixer.Sound('sounds/background_music.mp3'),
        'pm': ParticleManager(game),
        'fps_text': Text(game, 'FPS: 0', (10,10), 'small', WHITE)
    }

    state['background_music'].set_volume(game.volume)
    state['background_music'].play(-1)

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

def create_room(game):
    game.currentState.client.send({'create_room': 'new_room'})


def click_on_room(game, room_id):
    game.state.client.send({'join_room': room_id})
    Text(game=game, str=f'You are now in room {room_id}', position=(500,300),font_size='medium')

def create_connect_state(game):
    def update_client(msg):
        def create_ctext(room_id):
            CTEXT = ClickableText(game, on_click= click_on_room, args=[game,room_id], str=str(room_id))
            print(game.currentState.ui_container)
            game.currentState.ui_container.add_element(CTEXT)

        if 'room_id' in msg:
            game.thread_manager.do(create_ctext, msg['room_id'])
        
        if 'room_ids' in msg:
            for room_id in msg['room_ids']:
                game.thread_manager.do(create_ctext, room_id)
        
        if 'all_clients_connected' in msg:
            game.thread_manager.do(click_play, game)


    game.states['connect'].set(
        background=Background(game=game),
        
    )
    ROOMS_BUTTON = ClickableText(game, on_click=create_room, args=[game], str='Create Room')
    ROOMS_TEXT = Text(game, str='Rooms:')
    UI_POS = tuple(np.array(game.screen.get_size())/2)
    game.currentState.ui_container=UIContainer(game, UI_POS, elements=[ROOMS_BUTTON, ROOMS_TEXT], isCenter=True)
    
    try:
        game.currentState.client=Client(update_client, on_client_connect=lambda :click_play(game), wait_for_clients=False)
        game.currentState.client.send({'get_rooms':''})
    except Exception as e:
        print(e)

def click_connect_text(game):
    game.set_state('connect')

def create_menu_state(game):
    Background(game=game)
    MENU_UI_POSITION = list(map(lambda x: x/2, game.screen.get_size()))

    PLAY_TEXT = ClickableText(game, on_click=click_play, args=[game], str='Play')
    EDIT_DECK_TEXT = ClickableText(game, on_click=game.set_state, args=['buildDeck'], str='Edit Deck')
    CONNECT_TEXT = ClickableText(game, on_click=click_connect_text, args=[game], str='Connect')

    game.ui_container = UIContainer(game, MENU_UI_POSITION, elements=[PLAY_TEXT, EDIT_DECK_TEXT, CONNECT_TEXT],isCenter=True)
    
def start(game):
    game.thread_manager = ThreadManager()
    game.volume = .2 #from 0 to 1.0
    game.key_actions = {
        pygame.K_SPACE: lambda: game.currentState.get('passTurnButton', None) and game.currentState['passTurnButton'].on_click()
    }

    game.states = {
        'menu': GameState(game, 'menu', create_menu_state),
        'play': GameState(game, 'play'),
        'buildDeck': GameState(game, 'buildDeck', create_deck_builder_state, cardsToAdd = []),
        'connect': GameState(game, 'connect', create_connect_state)
    }
    game.set_state('menu')

def update(game):
    game.thread_manager.update()

    if game.currentState['pm']:
        game.currentState['pm'].update()

    if game.currentState['fps_text']:
        game.currentState['fps_text'].str = f'FPS: {int(game.clock.get_fps())}'

GAME = Game(start, update)

def get_attack_message(self, msg_obj):
    attacking_player_num = msg_obj['attacker']['player_num']
    defending_player_num = 1 - attacking_player_num  # Assuming 2 players only
    
    attacker = self.game.currentState['players'][attacking_player_num].field[msg_obj['attacker']['field_id']]
    defenders = []
    for defender_info in msg_obj['defenders']:
        defender_field_id = defender_info['field_id']
        if defender_field_id == 'player':
            defender = self.game.currentState['players'][defending_player_num]
        else:
            defender = self.game.currentState['players'][defending_player_num].field[defender_field_id]
        defenders.append(defender)
    
    return attacker, defenders
