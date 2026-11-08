"""Backwards-compatible entry point for the card game.

The implementation lives in the :mod:`card_game` package. This module keeps
``python main.py`` working and re-exports the functions that older code and
tests imported from the top level.
"""

from card_game.app import main, start, update
from card_game.core.players import (
    create_opponent_player,
    get_opponent,
    get_opponent_player_num,
    place_player_at_num,
)
from card_game.network.session import disconnect_client
from card_game.states.connect import (
    click_on_room,
    create_connect_state,
    create_room,
    show_in_room,
)
from card_game.states.deck_builder import (
    create_deck_builder_state,
    json_to_dictionary,
    save_and_exit,
    to_matrix,
)
from card_game.states.menu import (
    click_back_to_menu,
    click_connect_text,
    click_edit_deck_text,
    create_menu_state,
)
from card_game.states.play import (
    click_play,
    handle_game_message,
    on_click_leave_game,
    try_pass_turn,
)

__all__ = [
    'click_back_to_menu',
    'click_connect_text',
    'click_edit_deck_text',
    'click_on_room',
    'click_play',
    'create_connect_state',
    'create_deck_builder_state',
    'create_menu_state',
    'create_opponent_player',
    'create_room',
    'disconnect_client',
    'get_opponent',
    'get_opponent_player_num',
    'handle_game_message',
    'json_to_dictionary',
    'main',
    'on_click_leave_game',
    'place_player_at_num',
    'save_and_exit',
    'show_in_room',
    'start',
    'to_matrix',
    'try_pass_turn',
    'update',
]


if __name__ == '__main__':
    main()
