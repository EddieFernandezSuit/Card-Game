import pytest
from entities.Zone import Zone
from entities.player import Player

def test_click_with_no_selected_card_does_nothing(game):
    player = Player(game, 0)
    game.currentState['players'] = [player]
    game.currentState['selectedCard'] = None
    zone = Zone((0,0), 0, game)
    old_hand = player.hand.copy()
    zone.on_click()

    assert zone.isFull == 0
    assert player.field == []
    assert player.hand == old_hand

def test_click_with_zone_full(game):
    player = Player(game, 0)
    game.currentState['players'] = [player]
    game.currentState['selectedCard'] = player.hand[0]
    zone = Zone((0,0), 0, game)
    zone.isFull = 1
    old_hand = player.hand.copy()
    zone.on_click()

    assert player.field == []
    assert player.hand == old_hand

def test_wrong_players_card(game, player):
    game.currentState['players'] = [player]
    game.currentState['selectedCard'] = player.hand[0]
    zone = Zone(playerNum=1,game=game)
    old_hand = player.hand.copy()
    zone.on_click()

    assert zone.isFull == 0
    assert game.currentState['selectedCard'] == player.hand[0]
    assert player.field == []
    assert player.hand == old_hand

def test_success_play_card(game, player):
    game.currentState['players'] = [player]
    card = player.hand[0]
    game.currentState['selectedCard'] = card
    zone = Zone(game=game)
    zone.on_click()

    assert zone.isFull == 1
    assert game.currentState['selectedCard'] == None
    assert player.field[0] == card
    assert player.hand[0] != card