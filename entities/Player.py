import csv
import pygame
from entities.card import Card
from Game import Game
from entities.zone import Zone
from entities.entity import Entity
from entities.text import TextHandler
from entities.flying_num import FlyingNum
import random
import Colors
import json

class Player(Entity):
    def __init__(self, game, num) -> None:
        super().__init__(game)

        self.impaledArrows = []
        self.stats = {
            'Armor': 0,
            'Health': 20
        }
        self.armor = 0
        self.totalMana = int(num == 0)
        self.mana = int(num == 0)
        self.deck = []
        self.hand = []
        self.field = []
        self.zones = []
        self.num = num
        self.game = game
        UIBaseManaX = game.SCREEN_WIDTH - 250
        UIBaseManaY = [50, game.SCREEN_HEIGHT-100]
        self.healthText = TextHandler(game, 'Health: ' + str(self.stats['Health']), pygame.Vector2(UIBaseManaX, UIBaseManaY[self.num]), game.fonts['big'] )
        self.manaText = TextHandler(game, 'Mana: ' + str(self.mana) + '/' + str(self.totalMana), pygame.Vector2(UIBaseManaX, UIBaseManaY[self.num] + game.fonts['big'].size('1')[1]), game.fonts['big'] )
        
        self.handY = [5, self.game.SCREEN_HEIGHT - 205]
        fieldPositionY = [210, game.SCREEN_HEIGHT - 410]

        for y in range(5):
            self.zones.append(Zone(pygame.Vector2(cardPositionX(y), fieldPositionY[num]), num, game))

        def addCard(cardName):
            self.deck.append(Card(self.game, self.num, cardName))

        with open('DeckBox.json') as deckboxFile:
            deckBoxData = json.load(deckboxFile)
            deck = deckBoxData[list(deckBoxData.keys())[num]]
            for card in deck:
                quantity = card['quantity']
                cardName = card['name']
                for x in range(int(quantity)):
                    addCard(cardName)

        random.shuffle(self.deck)

        for x in range(4):
            self.drawCard()
    
    def drawCard(self):
        handPositionY = [5, self.game.SCREEN_HEIGHT - 205]
        self.hand.append(self.deck[-1])
        self.deck.pop(-1)
        self.hand[-1].transform_component.position.x = cardPositionX(len(self.hand)-1)
        self.hand[-1].transform_component.position.y = handPositionY[self.num]
        
    def update(self):
        self.manaText.str = 'Mana: ' + str(self.mana) + '/' + str(self.totalMana)
        for index, card in enumerate(self.hand):
            card.transform_component.position.x = cardPositionX(index)
            card.transform_component.position.y = self.handY[self.num]

    def delete(self):
        for player in self.game.currentState["players"]:
            if player.stats['Health'] <= 0:
                print('Player ' + str(player.num + 1) + ' wins')
                self.game = Game(self.game.start, self.game.update, self.game.draw)
    
    def setStat(self, statName, newStat):
        statChange = newStat - self.stats[statName]

        color = Colors.LIGHT_GREEN if statChange > 0 else Colors.LIGHT_RED

        FlyingNum(self.game, str(statChange ) + ' ' + statName, self.healthText.transform_component.position, color)
        self.stats[statName] = newStat
        self.healthText.str = statName + ' ' + str(self.stats[statName])

    def setMana(self, value):
        statChange = value - self.mana
        self.mana = value
        self.manaText.str = 'Mana: ' + str(self.mana) + '/' + str(self.totalMana)

def cardPositionX(i):
    return 5 + 210 * (i + 1)