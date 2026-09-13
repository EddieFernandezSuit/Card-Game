from entities.player import Player

def test_player_zero_starts_with_full_health(game):
    player = Player(game, 0, cards_in_deck=['Bird'])
    assert player.stats['Health'] == 20

def test_player_zero_starts_with_one_mana(game):
    player = Player(game, 0, cards_in_deck=['Bird'])
    assert player.stats['Mana'] == 1

def test_player_one_starts_with_zero_mana(game):
    player = Player(game, 1, cards_in_deck=['Bird'])
    assert player.stats['Mana'] == 0