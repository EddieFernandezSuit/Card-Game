from asyncio.windows_events import NULL
import pygame
import sys
import random
import Colors
from Game import Game
from Clicker import Clicker

class Card:
    def __init__(self, name, mana, damage, health, playerNum, game) -> None:
        self.x = 5
        self.y = 5
        self.name = name
        self.mana = mana
        self.damage = damage
        self.health = health
        self.image = pygame.image.load('jungle.jpg')
        self.rect = pygame.Rect(self.x,self.y,200,200)
        self.playerNum = playerNum
        self.place = 'hand'
        self.fieldPosition= 0
        self.attackUsed = 0
        self.clicker = Clicker(self.rect, self.onClick, (game))

    def onClick(self, game):
        if game.selectedCard == self:
            game.selectedCard = NULL
        elif game.selectedCard == NULL:
            if len(game.players[int(self.playerNum == 0)].field) == 0 and self.place == 'field' and self.attackUsed == 0:
                game.players[int(self.playerNum == 0)].health -= self.damage
            elif game.turn == self.playerNum and ((self.place == 'hand' and game.players[self.playerNum].mana >= self.mana and game.turn == self.playerNum) or (self.place == 'field' and self.attackUsed == 0)):
                game.selectedCard = self
        else:
            if self.place == 'field' and game.selectedCard.place == 'field':
                damage(game.selectedCard, self, game)
                game.selectedCard.attackUsed = 1
                game.selectedCard = NULL

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.clicker.update()

class EmptyZone:
    def __init__(self, x, y, playerNum, game):
        self.image = pygame.image.load('emptyZone.png')
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,200,200)
        self.isFull = 0
        self.playerNum = playerNum
        self.clicker = Clicker(self.rect, self.click, (game))
    
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

    
    def update(self):
        self.clicker.update()

class PassTurnButton:
    def __init__(self,game):
        self.image = pygame.image.load('PassTurn.png')
        self.x = game.SCREEN_WIDTH - 200
        self.y = game.SCREEN_HEIGHT/2 - 25
        self.rect = pygame.Rect(self.x,self.y,50,50)
        self.clicker = Clicker(self.rect, self.onClick, (game))

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

    def update(self):
        self.clicker.update()

class Player:
    def __init__(self, totalMana) -> None:
        self.health = 20
        self.totalMana = totalMana
        self.mana = 1
        self.deck = []
        self.hand = []
        self.field = []

def damage(damager,damaged,game):
    damaged.health -= damager.damage
    if damaged.health <= 0:
        game.players[damaged.playerNum].field.remove(damaged)
        game.cards.remove(damaged)

def drawOutlineText(game,str,x,y,):
    game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x + 1, y + 1))
    game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x - 1, y + 1))
    game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x + 1, y - 1))
    game.screen.blit(game.font.render(str, 1, Colors.BLACK), (x - 1, y - 1))
    game.screen.blit(game.font.render(str, 1, Colors.WHITE), (x, y))

def cardPositionX(i):
    return 5 + 205 * (i + 1)

def start(game):
    game.players = [Player(1), Player(0)]
    game.phase = 'play'
    game.passTurnButton = PassTurnButton(game)
    game.turn = 0
    game.turnRectangle = pygame.Rect(150, 0, 1150, 450)
    game.selectedCard = NULL

    for index, player in enumerate(game.players):
        for x in range(10):
            player.deck.append(Card('TGuy1', 1, 1, 1, index, game))
        for x in range(10):
            player.deck.append(Card('TGuy2', 2, 2, 2, index, game))
        for x in range(10):
            player.deck.append(Card('TGuy3', 3, 3, 3, index, game))
    
    for player in game.players:
        random.shuffle(player.deck)

    handPositionY = [5, game.SCREEN_HEIGHT - 205]
    fieldPositionY = [210, game.SCREEN_HEIGHT - 410]

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

    game.emptyZones = []

    for x in range(2):
        for y in range(5):
            game.emptyZones.append(EmptyZone(cardPositionX(y), fieldPositionY[x], x, game))

def update(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.passTurnButton.onClick(game)

    game.passTurnButton.update()
    for i in reversed(range(len(game.cards))):
        game.cards[i].update()

    for i in range(len(game.players[0].hand)):
        game.players[0].hand[i].x = cardPositionX(i)

    for i in range(len(game.players[1].hand)):
        game.players[1].hand[i].x = 5 + 205 * (i + 1)
        game.players[1].hand[i].y = game.SCREEN_HEIGHT - 205

    for i in reversed(range(len(game.emptyZones))):
        game.emptyZones[i].update()

def draw(game):
    def drawImage(object):
        game.screen.blit(object.image, (object.x, object.y))

    for x in range(len(game.emptyZones)):
        drawImage(game.emptyZones[x])

    for x in range(len(game.cards)):
        drawImage(game.cards[x])
        temp = [str(game.cards[x].name), 'M: ' + str(game.cards[x].mana), 'D: ' + str(game.cards[x].damage),
                'H: ' + str(game.cards[x].health)]
        for y in range(len(temp)):
            drawOutlineText(game, temp[y] ,game.cards[x].x + 5, game.cards[x].y + 5 + y * game.fontSize)
        
    if game.selectedCard != NULL:
        drawOutlineText(game,'X', game.selectedCard.x + 100, game.selectedCard.y +100)
    UIManaX = game.SCREEN_WIDTH - 200
    UIBaseManaY = [50, game.SCREEN_HEIGHT-100]

    for index, player in enumerate(game.players):
        drawOutlineText(game, 'Mana: ' + str(player.mana) + '/' + str(player.totalMana), UIManaX, UIBaseManaY[index])
        drawOutlineText(game, 'Health: ' + str(player.health), UIManaX, UIBaseManaY[index] + game.fontSize)
        
    drawImage(game.passTurnButton)

    drawOutlineText(game, str(game.turn), game.passTurnButton.x, game.passTurnButton.y - game.fontSize)
    drawOutlineText(game, str(game.phase), game.passTurnButton.x, game.passTurnButton.y- game.fontSize * 2)

    pygame.draw.rect(game.screen, Colors.BLACK, game.turnRectangle, 3)

Game(start, update, draw)
