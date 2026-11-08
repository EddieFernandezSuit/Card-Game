"""Application bootstrap and per-frame update hook."""

import pygame

from card_game.core.game import Game
from card_game.core.game_state import GameState
from card_game.states.connect import create_connect_state
from card_game.states.deck_builder import create_deck_builder_state
from card_game.states.menu import create_menu_state
from card_game.states.play import try_pass_turn


def start(game):
    game.volume = .2  # from 0 to 1.0
    game.key_actions = {
        pygame.K_SPACE: lambda: try_pass_turn(game),
    }

    game.states = {
        'menu': GameState(game, 'menu', create_menu_state),
        'play': GameState(game, 'play'),
        'buildDeck': GameState(
            game,
            'buildDeck',
            create_deck_builder_state,
            cardsToAdd=[],
        ),
        'connect': GameState(game, 'connect', create_connect_state),
    }
    game.set_state('menu')


def update(game):
    game.currentState.process_network()

    particle_manager = getattr(game.currentState, 'pm', None)
    if particle_manager:
        particle_manager.update()

    fps_text = getattr(game.currentState, 'fps_text', None)
    if fps_text:
        fps_text.str = f'FPS: {int(game.clock.get_fps())}'


def main():
    Game(start, update)
