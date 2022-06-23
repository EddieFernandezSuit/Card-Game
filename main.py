import pygame
import sys
import random
import Colors

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
    def __init__(self) -> None:
        self.health = 20
        self.totalMana = 1
        self.mana = 1
        self.deck = []
        self.hand = []
    
class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1600
        self.SCREEN_HEIGHT = 900
        self.fontSize = 25
        fontName = "freesansbold"
        self.myFont = pygame.font.SysFont(fontName, self.fontSize)
        self.resizeScreen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
        self.screen = self.resizeScreen.copy()
        # self.resizeScreen = pygame.display.set_mode((900,900), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
        self.start()
        while True:
            self.update()

    def start(self):
        self.players = [Player(), Player()]
        self.deleteCards = []
        self.phase = 'play'
        self.passTurnButton = PassTurnButton(self)
        self.turn = 0
        self.isSelected = 0

        for x in range(10):
            self.players[0].deck.append(Card('TGuy1', 1, 1, 1, 0))
        for x in range(10):
            self.players[0].deck.append(Card('TGuy2', 2, 2, 2,0))
        for x in range(10):
            self.players[0].deck.append(Card('TGuy3', 3, 3, 3,0))

        for x in range(10):
            self.players[1].deck.append(Card('TGuy1', 1, 1, 1,1))
        for x in range(10):
            self.players[1].deck.append(Card('TGuy2', 2, 2, 2,1))
        for x in range(10):
            self.players[1].deck.append(Card('TGuy3', 3, 3, 3,1))
        
        for player in self.players:
            random.shuffle(player.deck)

        def cardPositionx(i):
            return 5 + 205 * (i + 1)

        for i in range(5):
            self.players[0].deck[-1].x = cardPositionx(i)
            self.players[0].hand.append(self.players[0].deck[-1])
            self.players[0].deck.pop(-1)

        for i in range(5):
            self.players[1].deck[-1].x = cardPositionx(i)
            self.players[1].deck[-1].y = self.SCREEN_HEIGHT - 205
            self.players[1].hand.append(self.players[1].deck[-1])
            self.players[1].deck.pop(-1)

        self.cards = []

        for player in self.players:
            for card in player.hand:
                self.cards.append(card)

        self.emptyZones = []

        for i in range(5):
            self.emptyZones.append(EmptyZone(cardPositionx(i), 210, 0))
        for i in range(5):
            self.emptyZones.append(EmptyZone(cardPositionx(i), self.SCREEN_HEIGHT - 410,1))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    a = 1

        self.passTurnButton.update(self)
        for i in range(len(self.cards)):
            self.cards[i].update(self)

        for i in range(len(self.players[0].hand)):
            self.players[0].hand[i].x = 5 + 205 * (i + 1)

        for i in range(len(self.players[1].hand)):
            self.players[1].hand[i].x = 5 + 205 * (i + 1)
            self.players[1].hand[i].y = self.SCREEN_HEIGHT - 205

        if self.isSelected == 1 and self.phase == 'play':
            for i in range(len(self.emptyZones)):
                if pygame.mouse.get_pressed()[0] and self.emptyZones[i].rect.collidepoint(pygame.mouse.get_pos()) and self.emptyZones[i].isFull == 0:
                    for j in range(len(self.cards)):
                        if self.cards[j].isSelected == 1 and self.emptyZones[i].side == self.cards[j].side and self.phase == 'play' and self.cards[j].place == 'hand':
                            self.cards[j].place = 'field'
                            self.cards[j].x = self.emptyZones[i].x
                            self.cards[j].y = self.emptyZones[i].y
                            self.cards[j].isSelected = 0
                            if self.cards[j].side == 0:
                                for k in range(len(self.players[0].hand)):
                                    if self.players[0].hand[k] == self.cards[j]:
                                        self.players[0].hand.pop(k)
                                        break
                            else:
                                for k in range(len(self.players[1].hand)):
                                    if self.players[1].hand[k] == self.cards[j]:
                                        self.players[1].hand.pop(k)
                                        break
                            self.isSelected = 0
                            self.emptyZones[i].isFull = 1
                            if self.cards[j].side == 0:
                                self.players[0].mana -= self.cards[j].mana
                            else:
                                self.players[1].mana -= self.cards[j].mana

        for i in reversed(range(len(self.deleteCards))):
            print(i)
            self.cards.pop(self.deleteCards[i])
            self.deleteCards.pop(i)
        
        self.draw()

    def draw(self):
        self.screen.fill(Colors.GREY)

        for x in range(len(self.emptyZones)):
            self.screen.blit(self.emptyZones[x].image, (self.emptyZones[x].x, self.emptyZones[x].y))

        for x in range(len(self.cards)):
            self.screen.blit(self.cards[x].image, (self.cards[x].x, self.cards[x].y))
            temp = [str(self.cards[x].name), 'M: ' + str(self.cards[x].mana), 'D: ' + str(self.cards[x].damage),
                    'H: ' + str(self.cards[x].health)]
            for y in range(len(temp)):
                drawOutlineText(self, temp[y] ,self.cards[x].x + 5, self.cards[x].y + 5 + y * self.fontSize)

            if self.cards[x].isSelected:
                drawOutlineText(self,'X', self.cards[x].x + 100,self.cards[x].y +100)

        drawOutlineText(self, 'Mana: ' + str(self.players[0].mana) + '/' + str(self.players[0].totalMana), self.SCREEN_WIDTH - 200, 50)
        drawOutlineText(self, 'Health: ' + str(self.players[0].health), self.SCREEN_WIDTH - 200, 50 + self.fontSize)
        drawOutlineText(self, 'Mana: ' + str(self.players[1].mana) + '/' + str(self.players[1].totalMana), self.SCREEN_WIDTH - 200, self.SCREEN_HEIGHT-50)
        drawOutlineText(self, 'Health: ' + str(self.players[1].health), self.SCREEN_WIDTH - 200, self.SCREEN_HEIGHT-50 + self.fontSize)
        self.screen.blit(self.passTurnButton.image, (self.passTurnButton.x, self.passTurnButton.y))
        drawOutlineText(self, str(self.turn), self.passTurnButton.x, self.passTurnButton.y - self.fontSize)
        drawOutlineText(self, str(self.phase), self.passTurnButton.x, self.passTurnButton.y- self.fontSize * 2)
        
        pygame.display.update()
        self.resizeScreen.blit(pygame.transform.scale(self.screen, (self.resizeScreen.get_rect().size)), (0, 0))

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

game = Game()