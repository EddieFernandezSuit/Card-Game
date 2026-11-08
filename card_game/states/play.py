"""Play-state setup and network message handling."""

import pygame

from card_game.core.constants import WHITE
from card_game.core.particle_manager import ParticleManager
from card_game.core.paths import asset_path
from card_game.core.players import (
    create_opponent_player,
    get_opponent,
    place_player_at_num,
)
from card_game.entities.background import Background
from card_game.entities.clickable_text import ClickableText
from card_game.entities.pass_turn_button import PassTurnButton
from card_game.entities.player import Player
from card_game.entities.text import Text
from card_game.network.session import disconnect_client


def on_click_leave_game(game):
    """Stop the match and return to the main menu."""
    background_music = getattr(game.currentState, 'background_music', None)
    if background_music is not None:
        background_music.stop()

    client = getattr(game.currentState, 'client', None)
    if client is not None:
        disconnect_client(client)

    game.set_state('menu')


def try_pass_turn(game):
    """Pass the turn if the play state is active."""
    pass_turn_button = getattr(game.currentState, 'passTurnButton', None)
    if pass_turn_button is not None:
        pass_turn_button.on_click()


def handle_game_message(game, msg_obj):
    """Apply a message received from the opponent to the current match."""
    if 'player_left' in msg_obj:
        on_click_leave_game(game)
        return

    if 'deck' in msg_obj:
        create_opponent_player(game, msg_obj['deck'])

    if 'pass' in msg_obj:
        game.currentState.passTurnButton.pass_turn()

    if 'play' in msg_obj:
        card_name = msg_obj['play']
        opponent = get_opponent(game)
        card = opponent.get_card_in_hand(card_name)
        card.play()

    if 'attacker' in msg_obj:
        attacking_player_num = msg_obj['attacker']['player_num']
        attacking_card_field_id = msg_obj['attacker']['field_id']
        attacker = game.currentState.players[attacking_player_num].field[attacking_card_field_id]

        targets = []
        for target_info in msg_obj['targets']:
            target_player_num = target_info['player_num']
            target_player = game.currentState.players[target_player_num]
            target_field_id = target_info['field_id']
            if target_field_id == 'player':
                targets.append(target_player)
            else:
                targets.append(target_player.field[target_field_id])

        attacker.attack(targets)


def click_play(game):
    """Build the play state and start the match."""
    game.currentState = game.states['play']

    connect_state = game.states['connect']
    if hasattr(connect_state, 'client'):
        game.currentState.client = connect_state.client

    game.currentState.players = []
    game.get_opponent = get_opponent

    if hasattr(connect_state, 'client'):
        game.currentState.client.update_game_state = (
            lambda msg_obj: handle_game_message(game, msg_obj)
        )

    state = {
        'background': Background(game=game),
        'turn': 0,
        'passTurnButton': PassTurnButton(game),
        'selectedCard': None,
        'players': game.currentState.players,
        'arrowFlies': 0,
        'background_music': pygame.mixer.Sound(asset_path('sounds/background_music.mp3')),
        'pm': ParticleManager(game),
        'fps_text': Text(game, 'FPS: 0', (10, 10), 'small', WHITE),
        'leave_game_button': ClickableText(
            game,
            position=(game.SCREEN_WIDTH - 100, 10),
            str='Exit',
            on_click=on_click_leave_game,
            args=[game],
        ),
    }

    state['background_music'].set_volume(game.volume)
    state['background_music'].play(-1)

    game.currentState.update(state)

    # Created after the background so the local player's cards are not
    # blitted over by it (draw order = gameObjects insertion order).
    place_player_at_num(game, Player(game, game.currentState.client.client_id))
