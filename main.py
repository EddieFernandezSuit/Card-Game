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

UI_POSITION=(200,200)

def get_opponent_player_num(game):
    return game.currentState['client'].client_id == 0
    
def get_opponent(game):
    opponent_num = get_opponent_player_num(game)
    return game.currentState['players'][opponent_num]

def click_play(game):
    game.currentState = game.states['play']
    Background(game=game)
    game.get_opponent = get_opponent
    game.currentState['create_player_tm'] = ThreadManager()
    game.currentState['attack_tm'] = ThreadManager()

    def update_game_state(msg_obj):
        if 'deck' in msg_obj and ('players' not in game.currentState ):
                def create_player(deck):
                    game.currentState['players'].append(Player(game, game.currentState['client'].client_id == 0, deck))
                    if game.currentState['client'].client_id == 1:
                        game.currentState['players'].reverse()
                game.currentState['create_player_tm'].do(create_player, msg_obj['deck'])
        
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

            attacker = game.currentState['players'][attacking_player_num].field[attacking_card_field_id]
            if defending_card_field_id != 'player':
                target = game.currentState['players'][defending_player_num].field[defending_card_field_id]
            else:
                target = game.currentState['players'][defending_player_num]
            
            game.currentState['attack_tm'].do(lambda attacker, target: attacker.attack(target), attacker, target)
        
    game.currentState['client'] = Client(update_game_state)

    while not game.currentState['client'].is_all_clients_connected:
        pass

    state = {
        'turn': 0,
        'passTurnButton': PassTurnButton(game),
        'selectedCard': None,
        'players': [Player(game,game.currentState['client'].client_id)],
        'arrowFlies': 0,
        'select_text': TextSelector(game),
        'background_music': pygame.mixer.Sound('sounds/background_music.mp3').play(-1),
        'pm': ParticleManager(game),
        'fps_text': Text(game, 'FPS: 0', (10,10), 'small', WHITE)
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

def create_room(game):
    game.currentState.client.send({'port': 'new port'})


def click_on_room(game, port):
    # game.state.client.send({'create_server': port})
    pass

def create_connect_state(game):
    def update_client(msg_obj):
        def create_ctext(port):
            game.currentState.ui_container.add_element(ClickableText(game, click_on_room, args=[game,port], str=str(port)))

        if 'port' in msg_obj:
            game.thread_manager.do(create_ctext, msg_obj['port'])
        
        if 'ports' in msg_obj:
            for port in msg_obj['ports']:
                game.thread_manager.do(create_ctext, port)
            
            
    game.states['connect'].set(
        background=Background(game=game), 
        ui_container=UIContainer(game,UI_POSITION, elements=[
            ClickableText(game, on_click=create_room, args=[game], str='Create Room'),
            Text(game, str='Rooms:')
        ]),
    )

    game.currentState.client=Client(update_client, wait_for_clients=False)



def create_menu_state(game):
    Background(game=game)

    game.ui_container = UIContainer(game, UI_POSITION, elements=[
        ClickableText(game, on_click=click_play, args=[game], str='Play'),
        ClickableText(game, on_click=game.set_state, args=['buildDeck'], str='Edit Deck'),
        ClickableText(game, on_click=game.set_state, args=['connect'], str='Connect'),
    ])
    
def start(game):
    game.thread_manager = ThreadManager()
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
    
    if game.currentState['create_player_tm']:
        game.currentState['create_player_tm'].update()
    
    if game.currentState['attack_tm']:
        game.currentState['attack_tm'].update()

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