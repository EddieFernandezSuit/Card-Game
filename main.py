from asyncio.windows_events import NULL
import pygame
import sys
import random
import Colors
from Game import Game
from GameObject import GameObject
from Card import Card
from Handlers.TextHandler import TextHandler
from EmptyZone import EmptyZone
from PassTurnButton import PassTurnButton

class Player(GameObject):
    def __init__(self, game, num) -> None:
        super().__init__(game)
        self.position = pygame.Vector2()
        self.health = 20
        self.totalMana = int(num == 0)
        self.mana = 1
        self.deck = []
        self.hand = []
        self.field = []
        self.num = num
        self.game = game
        UIBaseManaX = game.SCREEN_WIDTH - 200
        UIBaseManaY = [50, game.SCREEN_HEIGHT-100]
        self.healthText = TextHandler(game, 'Health: ' + str(self.health), UIBaseManaX, UIBaseManaY[self.num],1, self)
        self.manaText = TextHandler(game, 'Mana: ' + str(self.mana) + '/' + str(self.totalMana), UIBaseManaX, UIBaseManaY[self.num] + game.font.size('1')[1], 1, self)

    def update(self):
        super().update()
        handY = [0, self.game.SCREEN_HEIGHT - 205]
        for index, card in enumerate(self.hand):
            card.position.x = 5 + 205 * (index + 1)
            card.position.y = handY[self.num]

def drawOutlineText(game,str,x,y,):
    game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x + 1, y + 1))
    game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x - 1, y + 1))
    game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x + 1, y - 1))
    game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x - 1, y - 1))
    game.screen.blit(game.font.render(str, 1, Colors.WHITE), (x, y))

def cardPositionX(i):
    return 5 + 205 * (i + 1)

def start(game):
    game.players = [Player(game,0), Player(game,1)]
    game.phase = 'play'
    game.passTurnButton = PassTurnButton(game)
    game.turn = 0
    game.turnRectangle = pygame.Rect(150, 0, 1150, 450)
    game.selectedCard = NULL
    handPositionY = [5, game.SCREEN_HEIGHT - 205]
    fieldPositionY = [210, game.SCREEN_HEIGHT - 410]
    game.emptyZones = []

    for x in range(2):
        for y in range(5):
            game.emptyZones.append(EmptyZone(pygame.Vector2(cardPositionX(y), fieldPositionY[x]), x, game))

    for index, player in enumerate(game.players):
        for x in range(10):
            player.deck.append(Card('TGuy1', 1, 1, 1, index, game))
        for x in range(10):
            player.deck.append(Card('TGuy2', 2, 2, 2, index, game))
        for x in range(10):
            player.deck.append(Card('TGuy3', 3, 3, 3, index, game))
    
    for player in game.players:
        random.shuffle(player.deck)

    for w, player in enumerate(game.players):
        for x in range(5):
            player.deck[-1].position.x = cardPositionX(w)
            player.deck[-1].position.y = handPositionY[w]
            player.hand.append(player.deck[-1])
            player.deck.pop(-1)

    game.cards = []

    for player in game.players:
        for card in player.hand:
            game.cards.append(card)


def update(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.passTurnButton.onClick(game)

def draw(game):
    if game.selectedCard != NULL:
        # drawOutlineText(game,'X', game.selectedCard.position.x + 100, game.selectedCard.position.y +100)
        drawOutlineText(game,'X', game.selectedCard.position.x + 100, game.selectedCard.position.y +100)

    pygame.draw.rect(game.screen, Colors.BLACK, game.turnRectangle, 3)

Game(start, update, draw)
