from entities.player import Player


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

    assert game.currentState['selectedCard'] is attacker
    assert game.currentState['arrowFlies'] == 0


def test_cannot_attack_own_card_from_player_one(field_clash):
    attacker, ally = field_clash(attacker_player_num=1, defender_player_num=1)

    ally.on_click()

    assert attacker.attackUsed == 0
    assert attacker.impaledArrows == []


def test_can_attack_opponent_card(field_clash, game):
    attacker, enemy = field_clash(attacker_player_num=0, defender_player_num=1)

    enemy.on_click()

    assert attacker.attackUsed == 1
    assert game.currentState['selectedCard'] is None
    assert game.currentState['arrowFlies'] == 1


def test_attacking_opponent_card_sends_message(field_clash, game):
    attacker, enemy = field_clash(attacker_player_num=0, defender_player_num=1)
    attacker_field_id = attacker.get_field_id(0)
    enemy_field_id = enemy.get_field_id(1)

    enemy.on_click()

    assert len(game.sent_messages) == 1
    message = game.sent_messages[0]
    assert message['attacker'] == {'player_num': 0, 'field_id': attacker_field_id}
    assert message['defender'] == {'player_num': 1, 'field_id': enemy_field_id}


def test_attacking_opponent_card_from_player_one_sends_message(field_clash, game):
    attacker, enemy = field_clash(attacker_player_num=1, defender_player_num=0)
    attacker_field_id = attacker.get_field_id(1)
    enemy_field_id = enemy.get_field_id(0)

    enemy.on_click()

    assert len(game.sent_messages) == 1
    message = game.sent_messages[0]
    assert message['attacker'] == {'player_num': 1, 'field_id': attacker_field_id}
    assert message['defender'] == {'player_num': 0, 'field_id': enemy_field_id}


def test_friendly_card_keeps_its_field_slot(field_clash, game):
    attacker, ally = field_clash(attacker_player_num=0, defender_player_num=0)
    player = game.currentState['players'][0]
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
