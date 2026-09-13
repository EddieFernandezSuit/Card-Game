import os

from entities.player import Player

os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

import pytest
from entities.Card import Card
from constants import FONT_SIZE_SMALL, FONT_SIZE_MEDIUM, FONT_SIZE_LARGE


class FakeClient:
    def send(self, message):
        pass


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
        self.currentState = {
            'gameObjects': [],
            'players': [],
            'client': FakeClient(),
        }


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