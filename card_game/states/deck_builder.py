"""Deck-builder state setup and persistence."""

import json
import os

import pygame

from card_game.core.paths import data_path, writable_data_path
from card_game.entities.background import Background
from card_game.entities.clickable_text import ClickableText
from card_game.entities.deck_box import DeckBox
from card_game.entities.deck_builder_card import DeckBuilderCard


def to_matrix(items, columns):
    """Split a flat list into rows of at most ``columns`` items."""
    return [items[i:i + columns] for i in range(0, len(items), columns)]


def json_to_dictionary(json_filename):
    with open(json_filename) as file:
        return json.load(file)


def create_deck_builder_state(game):
    game.currentState = game.states['buildDeck']

    Background(game)
    game.currentState.deckBox = DeckBox(game)

    card_data = json_to_dictionary(data_path('card_data.json'))
    deck_box_data = json_to_dictionary(data_path('decks.json'))

    columns = 3
    cards_in_matrix = to_matrix(
        [name for name in card_data.keys() if not name.startswith('_')],
        columns,
    )

    card_size = 200
    card_spacing = 10
    card_offset = card_size + card_spacing

    for row_index, row in enumerate(cards_in_matrix):
        for column_index, card_name in enumerate(row):
            position = (
                400 + column_index * card_offset,
                card_spacing + row_index * card_offset,
            )
            game.currentState.cardsToAdd.append(
                DeckBuilderCard(game, card_name, position)
            )

    for deck_cards in deck_box_data.values():
        game.currentState.deckBox.addDeck(deck_cards)

    game.currentState.save_and_exit = ClickableText(
        game,
        pygame.Vector2(
            10,
            game.SCREEN_HEIGHT - game.fonts['large'].size('A')[1] - 10,
        ),
        save_and_exit,
        [game],
        'Save and Exit',
    )


def save_and_exit(game):
    deck_box = {
        deck_list.deckName: deck_list.cards
        for deck_list in game.currentState.deckBox.deckLists
    }

    path = writable_data_path('decks.json')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as db:
        json.dump(deck_box, db)

    game.currentState = game.states['menu']
