import pygame
import pytest

from entities.Card import Card
from entities.player import Player


@pytest.fixture
def card(game):
    new_card = Card(game, 0, 'Bird')
    game.currentState['selectedCard'] = None
    return new_card


def blits_of(marker):
    marker.game.screen.blits.clear()
    marker.update()
    return marker.game.screen.blits


def test_marker_draws_when_its_card_is_selected(game, card):
    game.currentState['selectedCard'] = card

    assert len(blits_of(card.selected_marker)) == 5


def test_marker_does_not_draw_when_another_card_is_selected(game, card):
    other = Card(game, 1, 'Armadillo')
    game.currentState['selectedCard'] = other

    assert blits_of(card.selected_marker) == []
    assert len(blits_of(other.selected_marker)) == 5


def test_marker_does_not_draw_when_nothing_is_selected(game, card):
    game.currentState['selectedCard'] = None

    assert blits_of(card.selected_marker) == []


def test_marker_draws_after_its_own_card(game, card):
    game_objects = game.currentState['gameObjects']

    assert game_objects.index(card.selected_marker) > game_objects.index(card.image_component)
    assert game_objects.index(card.selected_marker) > game_objects.index(card)


def test_marker_draws_at_its_cards_center(game, card):
    game.currentState['selectedCard'] = card
    card.transform_component.position = pygame.Vector2(400, 300)
    card.transform_component.rect.topleft = card.transform_component.position

    blits = blits_of(card.selected_marker)

    assert pygame.Rect(blits[-1][1]).collidepoint(card.transform_component.rect.center)


def test_marker_follows_its_card_while_it_moves(game, card):
    game.currentState['selectedCard'] = card
    card.transform_component.position = pygame.Vector2(100, 100)
    card.transform_component.rect.topleft = card.transform_component.position
    card.transform_component.position = pygame.Vector2(700, 500)
    card.transform_component.rect.topleft = card.transform_component.position

    blits = blits_of(card.selected_marker)

    assert pygame.Rect(blits[-1][1]).collidepoint(card.transform_component.rect.center)
    assert card.transform_component.rect.center == (780, 580)


def test_marker_is_removed_when_its_card_is_deleted(game):
    player = Player(game, 0)
    game.currentState['players'] = [player]
    card = player.hand[0]
    card.emptyZone = player.zones[0]
    player.field.append(card)
    marker = card.selected_marker

    card.delete()

    assert marker not in game.currentState['gameObjects']
    assert card.image_component not in game.currentState['gameObjects']
