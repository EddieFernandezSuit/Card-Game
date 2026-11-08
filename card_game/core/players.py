"""Helpers for mapping players to their seats in a match."""

from card_game.entities.player import Player


def get_opponent_player_num(game):
    """Return the seat number (0 or 1) of the local player's opponent."""
    return 1 - game.currentState.client.client_id


def get_opponent(game):
    """Return the opponent's Player object."""
    return game.currentState.players[get_opponent_player_num(game)]


def place_player_at_num(game, player):
    """Insert a player into the state at the seat matching player.num."""
    players = game.currentState.players
    while len(players) <= player.num:
        players.append(None)
    players[player.num] = player


def create_opponent_player(game, deck):
    """Create the remote player once their deck has been received."""
    if not hasattr(game.currentState, 'players'):
        return

    players = game.currentState.players
    opponent_num = 1 - game.currentState.client.client_id
    while len(players) <= opponent_num:
        players.append(None)

    if players[opponent_num] is None:
        place_player_at_num(game, Player(game, opponent_num, deck))
