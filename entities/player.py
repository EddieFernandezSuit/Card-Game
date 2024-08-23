import pygame
from components.stats_component import StatsComponent
from entities.entity import Entity
from entities.card import Card
from entities.zone import Zone
from entities.text import Text
from constants import *
from Game import Game
import random
import json


class Player(Entity):
    def __init__(self, game, num, cards_in_deck=[], deck=[]) -> None:
        super().__init__(game)

        self.impaledArrows = []
        self.totalMana = int(num == 0)
        self.stats = {
            'Armor': 0,
            'Health': 20,
            'Mana': self.totalMana
        }
        self.stats_component = StatsComponent(self,self.stats)

        self.deck = []
        self.hand = []
        self.field = []
        self.zones = []
        self.num = num

        mana_ui_x_offset = 250
        mana_ui_x = game.SCREEN_WIDTH - mana_ui_x_offset
        ManaUI = [(mana_ui_x, 50), (mana_ui_x, game.SCREEN_HEIGHT - 100)]

        self.statsText = {
            'Health': Text(game, position=ManaUI[self.num], font_size='large'),
            'Mana': Text(game, position=(ManaUI[self.num][0], ManaUI[self.num][1] + FONTS['large'].size('1')[1]), font_size='large'),
        }

        self.transform_component = self.statsText['Health'].transform_component

        self.zones = [Zone((card_position(self.game, y, num, 'field')), num, game) for y in range(5)]

        if cards_in_deck:
            self.create_deck_using_names(cards_in_deck)
        else:
            self.create_deck_using_json('DeckBox.json')
        
        if not deck:
            self.send_deck()

        for _ in range(4):
            self.draw_card()


    def send_deck(self):
        card_names_deck = self.convert_deck_to_card_names()
        self.game.currentState['client'].send({'deck': card_names_deck})
    
    def create_deck_using_names(self, list_of_card_names):
        for card_name in list_of_card_names:
            self.deck.append(Card(self.game, self.num, card_name))

    def create_deck_using_json(self, file_name):
        with open(file_name) as deckboxFile:
            deckBoxData = json.load(deckboxFile)
            if self.num < len(deckBoxData):
                deck = deckBoxData[list(deckBoxData.keys())[self.num]]
                for card in deck:
                    quantity = card['quantity']
                    card_name = card['name']
                    for x in range(int(quantity)):
                        self.deck.append(Card(self.game, self.num, card_name))
        random.shuffle(self.deck)

    def draw_card(self):
        if self.deck:
            self.hand.append(self.deck[-1])
            self.deck.pop(-1)
            self.hand[-1].transform_component.position = card_position(self.game, (len(self.hand)-1), self.num)
        
    def update(self):
        self.statsText['Health'].str = f'Health: {self.stats["Health"]}'
        self.statsText['Mana'].str = f'Mana: {self.stats["Mana"]}/{self.totalMana}'
        for index, card in enumerate(self.hand):
            card.transform_component.position = card_position(self.game, index, self.num)

    def delete(self):
        print(f'Player {self.num + 1} wins')
        self.game.currentState['background_music'].stop()
        self.game = Game(self.game.start, self.game.update, self.game.draw)
    
    def convert_deck_to_card_names(self):
        list_of_card_names = [card.name for card in self.deck]
        return list_of_card_names
    
    def get_card_in_hand(self, name):
        for card in self.hand:
            if card.name == name:
                return card

def card_position(game, x_index, player_num, place = 'hand'):
    """
    Calculate the x position of a card based on its index in the hand.

    Args:
    i (int): The index of the card in the hand.
    card_width (int): The width of the card. Defaults to 210.
    padding (int): The padding between cards. Defaults to 5.

    Returns:
    int: The x position of the card.

    Raises:
    ValueError: If the index is not a non-negative integer.
    """

    card_size = CARD_SIZE
    PADDING = 10
    y_grid = 2 if place == 'field' else 1
    
    y_position = [(card_size + PADDING) * (y_grid - 1) + PADDING, game.SCREEN_HEIGHT - (card_size + PADDING) * y_grid - PADDING]
    return pygame.Vector2((PADDING + card_size) * (x_index + 1), y_position[player_num])
