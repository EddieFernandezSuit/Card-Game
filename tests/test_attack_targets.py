from types import SimpleNamespace

import pygame
from card_game.entities.player import Player
from card_game.entities.card import Card


def _make_board(game, attacker_name, enemy_names):
    players = [
        Player(game, 0, cards_in_deck=['Bird']),
        Player(game, 1, cards_in_deck=['Bird']),
    ]
    game.currentState.players = players
    game.get_opponent = lambda _: players[1]

    attacker = Card(game, 0, attacker_name)
    enemies = [Card(game, 1, name) for name in enemy_names]
    attacker.place = 'field'
    for enemy in enemies:
        enemy.place = 'field'
    players[0].field.append(attacker)
    players[1].field.extend(enemies)
    return attacker, enemies


def test_cannot_attack_own_card(field_clash):
    attacker, ally = field_clash(attacker_player_num=0, defender_player_num=0)
    ally_health = ally.stats['Health']

    ally.on_click()

    assert attacker.attackUsed == 0
    assert ally.stats['Health'] == ally_health
    assert attacker.impaledArrows == []
    assert ally.impaledArrows == []


def test_attacking_own_card_sends_no_message(field_clash, game):
    attacker, ally = field_clash(attacker_player_num=0, defender_player_num=0)

    ally.on_click()

    assert game.sent_messages == []


def test_attacking_own_card_leaves_it_selected(field_clash, game):
    attacker, ally = field_clash(attacker_player_num=0, defender_player_num=0)

    ally.on_click()

    assert game.currentState.selectedCard is attacker
    assert game.currentState.arrowFlies == 0


def test_cannot_attack_own_card_from_player_one(field_clash):
    attacker, ally = field_clash(attacker_player_num=1, defender_player_num=1)

    ally.on_click()

    assert attacker.attackUsed == 0
    assert attacker.impaledArrows == []


def test_can_attack_opponent_card(field_clash, game):
    attacker, enemy = field_clash(attacker_player_num=0, defender_player_num=1)

    enemy.on_click()

    assert attacker.attackUsed == 1
    assert game.currentState.selectedCard is None
    assert game.currentState.arrowFlies == 1


def test_attacking_opponent_card_sends_message(field_clash, game):
    attacker, enemy = field_clash(attacker_player_num=0, defender_player_num=1)
    attacker_field_id = attacker.get_field_id(0)
    enemy_field_id = enemy.get_field_id(1)

    enemy.on_click()

    assert len(game.sent_messages) == 1
    message = game.sent_messages[0]
    assert message['attacker'] == {'player_num': 0, 'field_id': attacker_field_id}
    assert message['targets'] == [{'player_num': 1, 'field_id': enemy_field_id}]


def test_attacking_opponent_card_from_player_one_sends_message(field_clash, game):
    attacker, enemy = field_clash(attacker_player_num=1, defender_player_num=0)
    attacker_field_id = attacker.get_field_id(1)
    enemy_field_id = enemy.get_field_id(0)

    enemy.on_click()

    assert len(game.sent_messages) == 1
    message = game.sent_messages[0]
    assert message['attacker'] == {'player_num': 1, 'field_id': attacker_field_id}
    assert message['targets'] == [{'player_num': 0, 'field_id': enemy_field_id}]


def test_friendly_card_keeps_its_field_slot(field_clash, game):
    attacker, ally = field_clash(attacker_player_num=0, defender_player_num=0)
    player = game.currentState.players[0]
    player.field.append(attacker)
    player.field.append(ally)
    attacker.emptyZone = player.zones[0]
    ally.emptyZone = player.zones[1]
    player.zones[0].isFull = 1
    player.zones[1].isFull = 1

    ally.on_click()

    assert player.field == [attacker, ally]
    assert player.zones[0].isFull == 1
    assert player.zones[1].isFull == 1


def test_splash_card_targets_first_cards(game):
    attacker, enemies = _make_board(game, 'Turtle', ['Bird', 'Bird', 'Bird'])

    assert attacker.get_attack_targets() == enemies[:2]


def test_single_enemy_is_targeted_without_splash(game):
    attacker, enemies = _make_board(game, 'Bird', ['Turtle'])

    assert attacker.get_attack_targets() == enemies


def test_empty_field_targets_the_opponent_player(game):
    attacker, _ = _make_board(game, 'Bird', [])

    assert attacker.get_attack_targets() == [game.currentState.players[1]]


def test_no_splash_requires_manual_target_with_multiple_enemies(game):
    attacker, _ = _make_board(game, 'Bird', ['Turtle', 'Turtle'])

    assert attacker.get_attack_targets() == []


def test_splash_attack_sends_one_message_with_all_targets(game):
    attacker, _ = _make_board(game, 'Turtle', ['Bird', 'Bird', 'Bird'])

    attacker.send_attack_message(attacker.get_attack_targets())

    assert game.sent_messages == [{
        'attacker': {'player_num': 0, 'field_id': 0},
        'targets': [
            {'player_num': 1, 'field_id': 0},
            {'player_num': 1, 'field_id': 1},
        ],
    }]


def test_attack_launches_one_arrow_per_target(game, monkeypatch):
    class FakeArrow:
        def __init__(self, game, origin, target):
            self.transform_component = SimpleNamespace(direction=pygame.Vector2(1, 0))

    monkeypatch.setattr('card_game.entities.card.Arrow', FakeArrow)
    attacker, enemies = _make_board(game, 'Turtle', ['Bird', 'Bird', 'Bird'])
    game.currentState.arrowFlies = 0
    original_position = attacker.transform_component.position.copy()

    attacker.attack(enemies[:2])
    attacker.transform_component.position += pygame.Vector2(20, 0)

    assert game.currentState.arrowFlies == 2
    assert attacker.before_position == original_position


def test_clicking_splash_card_attacks_all_targets_and_sends_one_message(game, monkeypatch):
    class FakeArrow:
        def __init__(self, game, origin, target):
            self.transform_component = SimpleNamespace(direction=pygame.Vector2(1, 0))

    monkeypatch.setattr('card_game.entities.card.Arrow', FakeArrow)
    attacker, enemies = _make_board(game, 'Turtle', ['Bird', 'Bird', 'Bird'])
    game.currentState.client.client_id = 0
    game.currentState.turn = 0
    game.currentState.selectedCard = None
    game.currentState.arrowFlies = 0

    attacker.on_click()

    assert game.currentState.arrowFlies == 2
    assert game.sent_messages == [{
        'attacker': {'player_num': 0, 'field_id': 0},
        'targets': [
            {'player_num': 1, 'field_id': 0},
            {'player_num': 1, 'field_id': 1},
        ],
    }]


