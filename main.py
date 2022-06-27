from asyncio.windows_events import NULL
from email.mime import image
import pygame
import sys
import random
import Colors
from Game import Game
from GameObject import GameObject
from handlers.Clicker import Clicker
from handlers.ImageHandler import ImageHandler
from Card import Card
from handlers.TextHandler import TextHandler

class EmptyZone(GameObject):
    def __init__(self, x, y, playerNum, game):
        super().__init__(game)
        self.imageHandler = ImageHandler(pygame.image.load('images/emptyZone.png'),self,game.screen)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,200,200)
        self.isFull = 0
        self.playerNum = playerNum
        self.clicker = Clicker(self.rect, self.click, (game), self)
    
    def click(self, game):
        if self.isFull == 0 and game.selectedCard != NULL and self.playerNum == game.selectedCard.playerNum and game.selectedCard.place == 'hand':
            game.selectedCard.place = 'field'
            game.players[self.playerNum].field.append(game.selectedCard)
            game.selectedCard.x = self.x
            game.selectedCard.y = self.y
            self.isFull = 1
            game.players[game.selectedCard.playerNum].mana -= game.selectedCard.mana
            for k in range(len(game.players[game.selectedCard.playerNum].hand)):
                if game.players[game.selectedCard.playerNum].hand[k] == game.selectedCard:
                    game.players[game.selectedCard.playerNum].hand.pop(k)
                    break
            game.selectedCard = NULL

class PassTurnButton(GameObject):
    def __init__(self,game):
        super().__init__(game)
        self.handlers = []
        self.x = game.SCREEN_WIDTH - 200
        self.y = game.SCREEN_HEIGHT/2 - 25
        self.rect = pygame.Rect(self.x,self.y,50,50)
        self.imageHandler = ImageHandler(pygame.image.load('images/PassTurn.png'), self, game.screen)
        self.clicker = Clicker(self.rect, self.onClick, (game), self)

    def onClick(self, game):
        for i in range(len(game.cards)):
            game.selectedCard = NULL
            game.cards[i].attackUsed = 0
        if game.phase == 'play':
            for j in range(len(game.emptyZones)):
                game.emptyZones[j].isFull = 0
                for i in range(len(game.cards)):
                    if game.cards[i].x == game.emptyZones[j].x and game.cards[i].y == game.emptyZones[j].y:
                        game.emptyZones[j].isFull = 1
            game.phase = 'play'
            game.turn = int(game.turn == 0)
            game.players[game.turn].totalMana += 1
            game.players[game.turn].mana = game.players[0].totalMana
            turnRectangleY = [0, 450]
            game.turnRectangle.y = turnRectangleY[game.turn]

class Player(GameObject):
    def __init__(self, game, num) -> None:
        super().__init__(game)
        self.x = 0
        self.y = 0
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
            card.x = 5 + 205 * (index + 1)
            card.y = handY[self.num]

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
            game.emptyZones.append(EmptyZone(cardPositionX(y), fieldPositionY[x], x, game))

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
            player.deck[-1].x = cardPositionX(w)
            player.deck[-1].y = handPositionY[w]
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

    # game.passTurnButton.update()

    # for i in reversed(range(len(game.emptyZones))):
    #     game.emptyZones[i].update()
        
    # for i in reversed(range(len(game.cards))):
    #     game.cards[i].update(game)
    
    # for player in game.players:
    #     player.update()

def draw(game):
    if game.selectedCard != NULL:
        drawOutlineText(game,'X', game.selectedCard.x + 100, game.selectedCard.y +100)

    pygame.draw.rect(game.screen, Colors.BLACK, game.turnRectangle, 3)

Game(start, update, draw)
