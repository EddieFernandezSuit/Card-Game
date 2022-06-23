import pygame
import sys
import random
import Colors
import Game

class Card:
    def __init__(self, name, mana, damage, health, side) -> None:
        self.x = 5
        self.y = 5
        self.name = name
        self.mana = mana
        self.damage = damage
        self.health = health
        self.image = pygame.image.load('jungle.jpg')
        self.rect = pygame.Rect(self.x,self.y,200,200)
        self.isSelected = 0
        self.lastClick = 0
        self.side = side
        self.place = 'hand'
        self.fieldPosition= 0
        self.attackUsed = 0

    def isClicked(self, game):
        if pygame.mouse.get_pressed()[0] and self.lastClick == 0 and self.rect.collidepoint(pygame.mouse.get_pos()) :
            if game.phase == 'play' and ((game.players[0].mana >= self.mana and self.side == 0) or (self.side == 1 and game.players[1].mana >= self.mana)) and game.turn == self.side :
                if game.isSelected == 0:
                    if self.isSelected == 0:
                        self.isSelected = 1
                        game.isSelected = 1
                elif game.isSelected == 1:
                    if self.isSelected == 1:
                        self.isSelected = 0
                        game.isSelected = 0
            elif game.phase == 'battle' and self.place == 'field':
                if game.isSelected == 1:
                    for i in range(len(game.cards)):
                        if game.cards[i].isSelected == 1 and game.cards[i].place == 'field' and game.cards[i] != self:
                            damage(game.cards[i], self, game)
                            game.isSelected = 0
                            game.cards[i].isSelected = 0
                            game.cards[i].attackUsed = 1
                            break
                elif game.isSelected == 0  and self.attackUsed == 0 and self.side == game.turn:
                    count = 0
                    for i in range(len(game.cards)):
                        if game.cards[i].side != self.side and game.cards[i].place == 'field':
                            count+=1
                    if count == 0:
                        self.attackUsed = 1
                        if self.side == 0:
                            game.player.health -= self.damage
                        elif self.side == 1:
                            game.players[0].health -= self.damage
                    else:
                        self.isSelected = 1
                        game.isSelected = 1


        self.lastClick = pygame.mouse.get_pressed()[0]


    def update(self, game):
        self.rect.x = self.x
        self.rect.y = self.y
        self.isClicked(game)

class EmptyZone:
    def __init__(self, x, y, side):
        self.image = pygame.image.load('emptyZone.png')
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,200,200)
        self.isFull = 0
        self.side = side

class PassTurnButton:
    def __init__(self,game):
        self.image = pygame.image.load('PassTurn.png')
        self.x = game.SCREEN_WIDTH - 200
        self.y = game.SCREEN_HEIGHT/2 - 25
        self.rect = pygame.Rect(self.x,self.y,50,50)
        self.lastClick = 0

    def isClicked(self, game):
        if pygame.mouse.get_pressed()[0] and self.lastClick == 0 and self.rect.collidepoint(pygame.mouse.get_pos()):
            for i in range(len(game.cards)):
                game.cards[i].isSelected = 0
                game.isSelected = 0
                game.cards[i].attackUsed = 0
            if game.phase == 'play':
                game.phase = 'battle'
            elif game.phase == 'battle':
                for j in range(len(game.emptyZones)):
                    game.emptyZones[j].isFull = 0
                    for i in range(len(game.cards)):
                        if game.cards[i].x == game.emptyZones[j].x and game.cards[i].y == game.emptyZones[j].y:
                            game.emptyZones[j].isFull = 1
                game.phase = 'play'
                if game.turn == 0:
                    game.turn = 1
                    game.players[1].totalMana += 1
                    game.players[1].mana = game.players[1].totalMana
                else:
                    game.turn = 0
                    game.players[0].totalMana += 1
                    game.players[0].mana = game.players[0].totalMana
        self.lastClick = pygame.mouse.get_pressed()[0]

    def update(self,game):
        self.isClicked(game)

class Player:
    def __init__(self, totalMana) -> None:
        self.health = 20
        self.totalMana = totalMana
        self.mana = 1
        self.deck = []
        self.hand = []

def damage(damager,damaged,game):
    damaged.health -= damager.damage
    if damaged.health <= 0:
        for i in range(len(game.cards)):
            if game.cards[i] == damaged:
                game.deleteCards.append(i)
                break

def drawOutlineText(game,str,x,y,):
    game.screen.blit(game.myFont.render(str, 1, Colors.BLACK),
                     (x + 1, y + 1))
    game.screen.blit(game.myFont.render(str, 1, Colors.BLACK),
                     (x - 1, y + 1))
    game.screen.blit(game.myFont.render(str, 1, Colors.BLACK),
                     (x + 1, y - 1))
    game.screen.blit(game.myFont.render(str, 1, Colors.BLACK),
                     (x - 1, y - 1))
    game.screen.blit(game.myFont.render(str, 1, Colors.WHITE),
                     (x, y))

def cardPositionX(i):
    return 5 + 205 * (i + 1)

def start(game):
    game.players = [Player(1), Player(0)]
    game.deleteCards = []
    game.phase = 'play'
    game.passTurnButton = PassTurnButton(game)
    game.turn = 0
    game.isSelected = 0

    for player in game.players:
        for x in range(10):
            player.deck.append(Card('TGuy1', 1, 1, 1, 0))
        for x in range(10):
            player.deck.append(Card('TGuy1', 2, 2, 2, 0))
        for x in range(10):
            player.deck.append(Card('TGuy1', 3, 3, 3, 0))
    
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
            game.emptyZones.append(EmptyZone(cardPositionX(y), fieldPositionY[x], 0))

def update(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                a = 1

    game.passTurnButton.update(game)
    for i in range(len(game.cards)):
        game.cards[i].update(game)

    for i in range(len(game.players[0].hand)):
        game.players[0].hand[i].x = cardPositionX(i)

    for i in range(len(game.players[1].hand)):
        game.players[1].hand[i].x = 5 + 205 * (i + 1)
        game.players[1].hand[i].y = game.SCREEN_HEIGHT - 205

    if game.isSelected == 1 and game.phase == 'play':
        for i in range(len(game.emptyZones)):
            if pygame.mouse.get_pressed()[0] and game.emptyZones[i].rect.collidepoint(pygame.mouse.get_pos()) and game.emptyZones[i].isFull == 0:
                for j in range(len(game.cards)):
                    if game.cards[j].isSelected == 1 and game.emptyZones[i].side == game.cards[j].side and game.phase == 'play' and game.cards[j].place == 'hand':
                        game.cards[j].place = 'field'
                        game.cards[j].x = game.emptyZones[i].x
                        game.cards[j].y = game.emptyZones[i].y
                        game.cards[j].isSelected = 0
                        if game.cards[j].side == 0:
                            for k in range(len(game.players[0].hand)):
                                if game.players[0].hand[k] == game.cards[j]:
                                    game.players[0].hand.pop(k)
                                    break
                        else:
                            for k in range(len(game.players[1].hand)):
                                if game.players[1].hand[k] == game.cards[j]:
                                    game.players[1].hand.pop(k)
                                    break
                        game.isSelected = 0
                        game.emptyZones[i].isFull = 1
                        if game.cards[j].side == 0:
                            game.players[0].mana -= game.cards[j].mana
                        else:
                            game.players[1].mana -= game.cards[j].mana

    for i in reversed(range(len(game.deleteCards))):
        print(i)
        game.cards.pop(game.deleteCards[i])
        game.deleteCards.pop(i)

def draw(game):
    for x in range(len(game.emptyZones)):
        game.screen.blit(game.emptyZones[x].image, (game.emptyZones[x].x, game.emptyZones[x].y))

    for x in range(len(game.cards)):
        game.screen.blit(game.cards[x].image, (game.cards[x].x, game.cards[x].y))
        temp = [str(game.cards[x].name), 'M: ' + str(game.cards[x].mana), 'D: ' + str(game.cards[x].damage),
                'H: ' + str(game.cards[x].health)]
        for y in range(len(temp)):
            drawOutlineText(game, temp[y] ,game.cards[x].x + 5, game.cards[x].y + 5 + y * game.fontSize)

        if game.cards[x].isSelected:
            drawOutlineText(game,'X', game.cards[x].x + 100,game.cards[x].y +100)

    drawOutlineText(game, 'Mana: ' + str(game.players[0].mana) + '/' + str(game.players[0].totalMana), game.SCREEN_WIDTH - 200, 50)
    drawOutlineText(game, 'Health: ' + str(game.players[0].health), game.SCREEN_WIDTH - 200, 50 + game.fontSize)
    drawOutlineText(game, 'Mana: ' + str(game.players[1].mana) + '/' + str(game.players[1].totalMana), game.SCREEN_WIDTH - 200, game.SCREEN_HEIGHT-50)
    drawOutlineText(game, 'Health: ' + str(game.players[1].health), game.SCREEN_WIDTH - 200, game.SCREEN_HEIGHT-50 + game.fontSize)
    game.screen.blit(game.passTurnButton.image, (game.passTurnButton.x, game.passTurnButton.y))
    drawOutlineText(game, str(game.turn), game.passTurnButton.x, game.passTurnButton.y - game.fontSize)
    drawOutlineText(game, str(game.phase), game.passTurnButton.x, game.passTurnButton.y- game.fontSize * 2)

game = Game.Game(start, update, draw)