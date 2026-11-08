"""Main-menu state setup."""

from card_game.entities.background import Background
from card_game.entities.clickable_text import ClickableText
from card_game.entities.ui_container import UIContainer
from card_game.network.session import disconnect_client


def click_edit_deck_text(game):
    game.set_state('buildDeck')


def click_connect_text(game):
    # Rebuild the connect state on every visit so the room list is fresh.
    game.states['connect'].is_state_created = False
    game.set_state('connect')


def click_back_to_menu(game):
    if hasattr(game.currentState, 'client'):
        disconnect_client(game.currentState.client)
    game.set_state('menu')


def create_menu_state(game):
    Background(game=game)
    menu_ui_position = list(map(lambda value: value / 2, game.screen.get_size()))

    edit_deck_text = ClickableText(
        game,
        on_click=click_edit_deck_text,
        args=[game],
        str='Edit Deck',
    )
    connect_text = ClickableText(
        game,
        on_click=click_connect_text,
        args=[game],
        str='Connect',
    )

    game.ui_container = UIContainer(
        game,
        menu_ui_position,
        elements=[edit_deck_text, connect_text],
        isCenter=True,
    )
