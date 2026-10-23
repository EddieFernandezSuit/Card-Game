import os

from entities.player import Player

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

import pytest
from entities.card import Card
from constants import FONT_SIZE_SMALL, FONT_SIZE_MEDIUM, FONT_SIZE_LARGE


class FakeClient:
    def send(self, message):
        pass


class RecordingScreen:
    """Stand-in for the pygame display that records what gets blitted."""

    def __init__(self):
        self.blits = []

    def blit(self, image, position):
        self.blits.append((image, tuple(position)))


class FakeGame:
    def __init__(self):
        self.SCREEN_WIDTH = 1500
        self.SCREEN_HEIGHT = 750
        self.volume = 0.2
        self.fonts = {
            'small': pygame.font.SysFont('freesansbold', FONT_SIZE_SMALL),
            'medium': pygame.font.SysFont('freesansbold', FONT_SIZE_MEDIUM),
            'large': pygame.font.SysFont('freesansbold', FONT_SIZE_LARGE),
        }
        self.screen = RecordingScreen()
        self.currentState = {
            'gameObjects': [],
            'players': [],
            'client': FakeClient(),
        }
        self.sent_messages = []

    def send(self, message):
        self.sent_messages.append(message)


@pytest.fixture
def game():
    return FakeGame()

@pytest.fixture
def player(game):
    return Player(game, 0)

@pytest.fixture
def deal_damage_shallow(game):
    def _attack(attacker_name, defender_name):
        attacker = Card(game, 0, attacker_name)
        defender = Card(game, 1, defender_name)
        attacker.deal_damage(defender)
        return attacker, defender
    return _attack

@pytest.fixture
def field_clash(game):
    def _setup(attacker_player_num=0, defender_player_num=1):
        players = [Player(game, 0), Player(game, 1)]
        game.currentState['players'] = players
        game.currentState['selectedCard'] = None
        game.currentState['arrowFlies'] = 0

        attacker = players[attacker_player_num].hand[0]
        defender = next(card for card in players[defender_player_num].hand if card is not attacker)
        for card in (attacker, defender):
            card.place = 'field'

        game.currentState['selectedCard'] = attacker
        return attacker, defender
    return _setup
