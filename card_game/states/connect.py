"""Lobby/connect state setup and room-list message handling."""

import numpy as np

from card_game.core.players import create_opponent_player
from card_game.entities.background import Background
from card_game.entities.clickable_text import ClickableText
from card_game.entities.text import Text
from card_game.entities.ui_container import UIContainer
from card_game.network.network import Client
from card_game.network.session import disconnect_client
from card_game.states.menu import click_back_to_menu
from card_game.states.play import click_play


def create_room(game):
    game.currentState.client.send({'create_room': 'new_room'})


def show_in_room(game, room_id):
    if not hasattr(game.currentState, 'YOU_ARE_IN_ROOM_TEXT'):
        game.currentState.YOU_ARE_IN_ROOM_TEXT = Text(
            game=game,
            str=f'You are now in room {room_id}',
            font_size='medium',
        )
        game.currentState.ui_container.insert_element(
            0,
            game.currentState.YOU_ARE_IN_ROOM_TEXT,
        )
    else:
        game.currentState.YOU_ARE_IN_ROOM_TEXT.str = (
            f'You are now in room {room_id}'
        )


def click_on_room(game, room_id):
    show_in_room(game, room_id)
    game.currentState.client.send({'join_room': room_id})


def update_lobby(game, msg):
    """Apply a message received from the server while in the lobby."""
    def create_room_text(room_id):
        room_text = ClickableText(
            game,
            on_click=click_on_room,
            args=[game, room_id],
            str=str(room_id),
        )
        game.currentState.ui_container.add_element(room_text)

    if 'room_id' in msg:
        create_room_text(msg['room_id'])

    if 'room_ids' in msg:
        for room_id in msg['room_ids']:
            create_room_text(room_id)

    if 'all_clients_connected' in msg:
        click_play(game)

    if 'deck' in msg:
        create_opponent_player(game, msg['deck'])

    if 'joined_room' in msg:
        show_in_room(game, msg['joined_room'])


def create_connect_state(game):
    # This state rebuilds on every visit: drop leftover entities and any
    # connection from the previous session so the room list starts fresh.
    game.currentState.gameObjects.clear()
    if hasattr(game.currentState, 'YOU_ARE_IN_ROOM_TEXT'):
        delattr(game.currentState, 'YOU_ARE_IN_ROOM_TEXT')

    if hasattr(game.currentState, 'client'):
        disconnect_client(game.currentState.client)

    game.states['connect'].set(background=Background(game=game))

    back_button = ClickableText(
        game,
        on_click=click_back_to_menu,
        args=[game],
        str='Back',
    )
    rooms_button = ClickableText(
        game,
        on_click=create_room,
        args=[game],
        str='Create Room',
    )
    rooms_text = Text(game, str='Rooms:')
    ui_position = tuple(np.array(game.screen.get_size()) / 2)
    game.currentState.ui_container = UIContainer(
        game,
        ui_position,
        elements=[back_button, rooms_button, rooms_text],
        isCenter=True,
    )

    try:
        game.currentState.client = Client(
            update_game_state=lambda msg: update_lobby(game, msg),
            on_client_connect=lambda: click_play(game),
            wait_for_clients=False,
        )
        game.currentState.client.send({'get_rooms': ''})
    except Exception as error:
        print(error)
