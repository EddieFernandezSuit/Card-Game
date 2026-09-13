import pytest
from entities.player import Player
from entities.Card  import Card


@pytest.mark.parametrize('attacker_name, defender_name, expected_health', [
    ('Bird', 'Bird', 2),
    ('Jungle Delver', 'Armadillo', 5),
    ('Shark', 'Armadillo', 3),
    ('Bats', 'Armadillo', 2),
])
def test_attacker_damages_defender(deal_damage_shallow, attacker_name, defender_name, expected_health):
    _, defender = deal_damage_shallow(attacker_name, defender_name)
    assert defender.stats['Health'] == expected_health

def test_bat_heals_itself_when_dealing_damage(deal_damage_shallow):
    attacker, _ = deal_damage_shallow('Bats', 'Armadillo')
    assert attacker.stats['Health'] == 4

def test_death(game):
    player = Player(game, 0)
    attacker = Card(game, 0 , 'Jungle Delver')
    player.field.append(attacker)

    def_player = Player(game, 1)
    defender = Card(game, 1, 'Jungle Delver')
    defender.emptyZone = def_player.zones[0]
    def_player.field.append(defender)

    game.currentState['players'] = [player,def_player]
    
    attacker.deal_damage(defender)

    assert def_player.field == []
    assert attacker.stats['Health'] == 2
    assert def_player.zones[0].isFull == 0

def test_devour(game):
    player = Player(game, 0)
    attacker = Card(game, 0 , 'Shark')
    player.field.append(attacker)

    def_player = Player(game, 1)
    defender = Card(game, 1, 'Jungle Delver')
    defender.emptyZone = def_player.zones[0]
    def_player.field.append(defender)

    game.currentState['players'] = [player,def_player]
    
    attacker.deal_damage(defender)

    assert def_player.field == []
    assert attacker.stats['Health'] == 8
    assert attacker.stats['Devour'] == 2
    assert def_player.zones[0].isFull == 0
