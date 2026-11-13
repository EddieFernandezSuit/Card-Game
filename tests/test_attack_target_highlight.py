import pygame
import pytest

from card_game.entities.player import Player


@pytest.fixture
def board(game):
    players = [Player(game, 0), Player(game, 1)]
    game.currentState.players = players
    game.currentState.selectedCard = None
    game.currentState.arrowFlies = 0

    attacker = players[0].hand[0]
    target = players[1].hand[0]
    for card in (attacker, target):
        card.place = 'field'
    players[0].field.append(attacker)
    players[1].field.append(target)
    return players, attacker, target


def blits_of(marker):
    marker.game.screen.blits.clear()
    marker.update()
    return marker.game.screen.blits


def test_enemy_card_is_highlighted_when_an_attacker_is_selected(game, board):
    _, attacker, target = board
    game.currentState.selectedCard = attacker

    assert len(blits_of(target.target_highlight)) == 1


def test_enemy_card_is_not_highlighted_without_a_selection(game, board):
    _, _, target = board

    assert blits_of(target.target_highlight) == []


def test_friendly_card_is_not_highlighted(game, board):
    players, attacker, _ = board
    ally = players[0].hand[1]
    ally.place = 'field'
    players[0].field.append(ally)
    game.currentState.selectedCard = attacker

    assert blits_of(ally.target_highlight) == []


def test_target_is_not_highlighted_when_the_selected_card_is_in_hand(game, board):
    _, attacker, target = board
    attacker.place = 'hand'
    game.currentState.selectedCard = attacker

    assert blits_of(target.target_highlight) == []


def test_target_is_not_highlighted_after_the_attacker_has_attacked(game, board):
    _, attacker, target = board
    attacker.attackUsed = 1
    game.currentState.selectedCard = attacker

    assert blits_of(target.target_highlight) == []


def test_card_in_hand_is_not_highlighted(game, board):
    _, attacker, target = board
    target.place = 'hand'
    game.currentState.selectedCard = attacker

    assert blits_of(target.target_highlight) == []


def test_selected_card_is_not_highlighted_as_its_own_target(game, board):
    _, attacker, _ = board
    game.currentState.selectedCard = attacker

    assert blits_of(attacker.target_highlight) == []


def test_highlight_draws_over_the_target_card(game, board):
    _, attacker, target = board
    game.currentState.selectedCard = attacker
    target.transform_component.position = pygame.Vector2(400, 300)
    target.transform_component.rect.topleft = target.transform_component.position

    blits = blits_of(target.target_highlight)

    image, position = blits[-1]
    assert pygame.Rect(position, image.get_size()).collidepoint(target.transform_component.rect.center)


def test_highlight_is_removed_when_its_card_is_deleted(game, board):
    players, _, target = board
    target.emptyZone = players[1].zones[0]
    target.emptyZone.isFull = 1
    highlight = target.target_highlight

    target.delete()

    assert highlight not in game.currentState.gameObjects
