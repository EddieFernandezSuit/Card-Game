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

def place_player_at_num(game, player):
    players = game.currentState['players']
    while len(players) <= player.num:
        players.append(None)
    players[player.num] = player

def create_opponent_player(game, deck):
    if 'players' not in game.currentState:
        return
    players = game.currentState['players']
    opponent_num = 1 - game.currentState['client'].client_id
    while len(players) <= opponent_num:
        players.append(None)
    if players[opponent_num] is None:
        place_player_at_num(game, Player(game, opponent_num, deck))

def disconnect_client(client):
    # The opponent leaving at the same time can close this socket from
    # the receive thread mid-teardown, so tolerate socket failures here
    try:
        client.update_game_state = lambda _: None
        client.send({'leave_game': ''})
        client.client.close()
    except OSError:
        pass

def on_click_leave_game(game: Game):
    if 'background_music' in game.currentState:
        game.currentState['background_music'].stop()
    if 'client' in game.currentState:
        disconnect_client(game.currentState['client'])
    game.set_state('menu')

def click_play(game):
    game.currentState = game.states['play']
    if 'client' in game.states['connect']:
        game.currentState['client'] = game.states['connect'].client
    game.currentState['players'] = []
    game.get_opponent = get_opponent

    def update_game_state(msg_obj):
        print('msg', msg_obj)
        if 'player_left' in msg_obj:
            if 'background_music' in game.currentState:
                game.currentState['background_music'].stop()
            if 'client' in game.currentState:
                disconnect_client(game.currentState['client'])
            game.set_state('menu')
            return
        if 'deck' in msg_obj:
            game.thread_manager.do(create_opponent_player, game, msg_obj['deck'])

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
        'players': game.currentState['players'],
        'arrowFlies': 0,
        'select_text': TextSelector(game),
        'background_music': pygame.mixer.Sound('sounds/background_music.mp3'),
        'pm': ParticleManager(game),
        'fps_text': Text(game, 'FPS: 0', (10,10), 'small', WHITE),
        'leave_game_button': ClickableText(game, position=(game.SCREEN_WIDTH - 100, 10), str='Exit', on_click=on_click_leave_game, args=[game])
    }

    state['background_music'].set_volume(game.volume)
    state['background_music'].play(-1)

    game.currentState.update(state)

    # Created after the background so the local player's cards are not
    # blitted over by it (draw order = gameObjects insertion order)
    place_player_at_num(game, Player(game, game.currentState['client'].client_id))

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
    cards_in_matrix = to_matrix([k for k in card_data.keys() if not k.startswith('_')], collumns)

    card_size = 200
    card_spacing = 10
    card_offset = card_size + card_spacing

    for i, row in enumerate(cards_in_matrix):
        for j, card in enumerate(row):
            deck_builder_card = DeckBuilderCard(game, card, (400 + j * card_offset, card_spacing + i * card_offset))
            game.currentState['cardsToAdd'].append(deck_builder_card)

    for key, deck_cards in deck_box_data.items():
        deck_list = game.currentState['deckBox'].addDeck(deck_cards)
        # deck_list.cards.extend(deck_cards)

    game.currentState['save and exit'] = ClickableText(game, pygame.Vector2(10, game.SCREEN_HEIGHT - FONTS['large'].size('A')[1] - 10), save_and_exit, [game], 'Save and Exit')
    # game.currentState = game.states['menu']

def save_and_exit(game):
    deckBox = {deckList.deckName: deckList.cards for deckList in game.currentState['deckBox'].deckLists}

    with open('DeckBox.json', 'w') as db:
        json.dump(deckBox, db)

    game.currentState = game.states['menu']

def create_room(game):
    game.currentState.client.send({'create_room': 'new_room'})
    # click_on_room(game, len(game.currentState.ui_container.elements) - 3)

def click_on_room(game, room_id):
    if 'YOU_ARE_IN_ROOM_TEXT' not in game.currentState:
        game.currentState.YOU_ARE_IN_ROOM_TEXT = Text(game=game, str=f'You are now in room {room_id}', font_size='medium')
        game.currentState.ui_container.insert_element(0, game.currentState.YOU_ARE_IN_ROOM_TEXT)
    else:
        game.currentState.YOU_ARE_IN_ROOM_TEXT.str = f'You are now in room {room_id}'
    game.currentState.client.send({'join_room': room_id})


def create_connect_state(game):
    # This state rebuilds on every visit: drop leftover entities and any
    # connection from the previous session so the room list starts fresh
    game.currentState.gameObjects.clear()
    if hasattr(game.currentState, 'YOU_ARE_IN_ROOM_TEXT'):
        delattr(game.currentState, 'YOU_ARE_IN_ROOM_TEXT')
    if 'client' in game.currentState:
        disconnect_client(game.currentState['client'])

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

        if 'deck' in msg:
            game.thread_manager.do(create_opponent_player, game, msg['deck'])


    game.states['connect'].set(
        background=Background(game=game),
    )
    BACK_BUTTON = ClickableText(game, on_click=click_back_to_menu, args=[game], str='Back')
    ROOMS_BUTTON = ClickableText(game, on_click=create_room, args=[game], str='Create Room')
    ROOMS_TEXT = Text(game, str='Rooms:')
    UI_POS = tuple(np.array(game.screen.get_size())/2)
    game.currentState.ui_container=UIContainer(game, UI_POS, elements=[BACK_BUTTON, ROOMS_BUTTON, ROOMS_TEXT], isCenter=True)

    try:
        game.currentState.client=Client(update_game_state=update_client, on_client_connect=lambda :click_play(game), wait_for_clients=False)
        game.currentState.client.send({'get_rooms':''})
    except Exception as e:
        print(e)

def click_edit_deck_text(game):
    game.set_state('buildDeck')

def click_connect_text(game):
    # Rebuild the connect state on every visit so the room list is fresh
    game.states['connect'].is_state_created = False
    game.set_state('connect')

def click_back_to_menu(game):
    if 'client' in game.currentState:
        disconnect_client(game.currentState['client'])
    game.set_state('menu')

def create_menu_state(game):
    Background(game=game)
    MENU_UI_POSITION = list(map(lambda x: x/2, game.screen.get_size()))

    # PLAY_TEXT = ClickableText(game, on_click=click_play, args=[game], str='Play')
    EDIT_DECK_TEXT = ClickableText(game, on_click=click_edit_deck_text, args=[game], str='Edit Deck')
    CONNECT_TEXT = ClickableText(game, on_click=click_connect_text, args=[game], str='Connect')

    game.ui_container = UIContainer(game, MENU_UI_POSITION, elements=[EDIT_DECK_TEXT, CONNECT_TEXT],isCenter=True)



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

GAME = Game(start, update)
