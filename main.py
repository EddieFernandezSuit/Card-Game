import pygame
import sys
import random
import Colors

def damage(damager,damaged,game):
    damaged.health -= damager.damage
    if damaged.health <= 0:
        for i in range(len(game.cards)):
            if game.cards[i] == damaged:
                game.deleteCards.append(i)
                break

class Card:
    def __init__(self, name, mana, damage, health, side):
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
            if game.phase == 'play' and ((game.mana1 >= self.mana and self.side == 0) or (self.side == 1 and game.mana2 >= self.mana)) and game.turn == self.side :
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
                            game.health2 -= self.damage
                        elif self.side == 1:
                            game.health1 -= self.damage
                    else:
                        self.isSelected = 1
                        game.isSelected = 1


        self.lastClick = pygame.mouse.get_pressed()[0]


    def update(self, game):
        self.rect.x = self.x
        self.rect.y = self.y
        self.isClicked(game)

class EmptyZone:
    def __init__(self,x,y,side):
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
                    game.totalMana2 += 1
                    game.mana2 = game.totalMana2
                else:
                    game.turn = 0
                    game.totalMana1 += 1
                    game.mana1 = game.totalMana1
        self.lastClick = pygame.mouse.get_pressed()[0]

    def update(self,game):
        self.isClicked(game)

def drawOutlineText(game,str,x,y,):
    game.screen.blit(game.myFont.render(str, 1, game.colors.BLACK),
                     (x + 1, y + 1))
    game.screen.blit(game.myFont.render(str, 1, game.colors.BLACK),
                     (x - 1, y + 1))
    game.screen.blit(game.myFont.render(str, 1, game.colors.BLACK),
                     (x + 1, y - 1))
    game.screen.blit(game.myFont.render(str, 1, game.colors.BLACK),
                     (x - 1, y - 1))
    game.screen.blit(game.myFont.render(str, 1, game.colors.WHITE),
                     (x, y))



class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH =1600
        self.SCREEN_HEIGHT = 900
        self.clock = pygame.time.Clock()
        self.fontSize = 25
        self.myFont = pygame.font.SysFont("freesansbold", self.fontSize)
        self.start(self)
        while True:
            self.update(self)
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.screen.fill(Colors.GREY)
            self.draw(self)
            pygame.display.update()
            self.clock.tick(60)

    def start(game):
        game.health1 = 20
        game.health2 = 20
        game.deleteCards = []
        game.phase = 'play'
        game.passTurnButton = PassTurnButton(game)
        game.turn = 0
        game.totalMana1 = 1
        game.totalMana2 = 0
        game.mana1 = 1
        game.mana2 = 0
        game.isSelected = 0
        game.deck1 = []
        game.deck2 = []
        for x in range(10):
            game.deck1.append(Card('TGuy1', 1, 1, 1, 0))
        for x in range(10):
            game.deck1.append(Card('TGuy2', 2, 2, 2,0))
        for x in range(10):
            game.deck1.append(Card('TGuy3', 3, 3, 3,0))
        for x in range(10):
            game.deck2.append(Card('TGuy1', 1, 1, 1,1))
        for x in range(10):
            game.deck2.append(Card('TGuy2', 2, 2, 2,1))
        for x in range(10):
            game.deck2.append(Card('TGuy3', 3, 3, 3,1))
        random.shuffle(game.deck1)
        random.shuffle(game.deck2)

        game.hand1 = []
        game.hand2 = []

        for i in range(5):
            game.deck1[-1].x = 5 + 205 * (i + 1)
            game.hand1.append(game.deck1[-1])
            game.deck1.pop(-1)

        for i in range(5):
            game.deck2[-1].x = 5 + 205 * (i + 1)
            game.deck2[-1].y = game.SCREEN_HEIGHT - 205
            game.hand2.append(game.deck2[-1])
            game.deck2.pop(-1)

        for x in range(len(game.deck1)):
            print(game.deck1[x].name)

        game.cards = []
        for x in range(len(game.hand1)):
            game.cards.append(game.hand1[x])
        for i in range(len(game.hand2)):
            game.cards.append(game.hand2[i])

        game.emptyZones = []
        for i in range(5):
            game.emptyZones.append(EmptyZone(5 + (i+1) * 205, 210,0))
        for i in range(5):
            game.emptyZones.append(EmptyZone(5 + (i+1) * 205, game.SCREEN_HEIGHT - 410,1))

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

        for i in range(len(game.hand1)):
            game.hand1[i].x = 5 + 205 * (i + 1)

        for i in range(len(game.hand2)):
            game.hand2[i].x = 5 + 205 * (i + 1)
            game.hand2[i].y = game.SCREEN_HEIGHT - 205

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
                                for k in range(len(game.hand1)):
                                    if game.hand1[k] == game.cards[j]:
                                        game.hand1.pop(k)
                                        break
                            else:
                                for k in range(len(game.hand2)):
                                    if game.hand2[k] == game.cards[j]:
                                        game.hand2.pop(k)
                                        break
                            game.isSelected = 0
                            game.emptyZones[i].isFull = 1
                            if game.cards[j].side == 0:
                                game.mana1 -= game.cards[j].mana
                            else:
                                game.mana2 -= game.cards[j].mana


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

        drawOutlineText(game, 'Mana: ' + str(game.mana1) + '/' + str(game.totalMana1), game.SCREEN_WIDTH - 200, 50)
        drawOutlineText(game, 'Health: ' + str(game.health1), game.SCREEN_WIDTH - 200, 50 + game.fontSize)
        drawOutlineText(game, 'Mana: ' + str(game.mana2) + '/' + str(game.totalMana2), game.SCREEN_WIDTH - 200, game.SCREEN_HEIGHT-50)
        drawOutlineText(game, 'Health: ' + str(game.health2), game.SCREEN_WIDTH - 200, game.SCREEN_HEIGHT-50 + game.fontSize)
        game.screen.blit(game.passTurnButton.image, (game.passTurnButton.x, game.passTurnButton.y))
        drawOutlineText(game, str(game.turn), game.passTurnButton.x, game.passTurnButton.y - game.fontSize)
        drawOutlineText(game, str(game.phase), game.passTurnButton.x, game.passTurnButton.y- game.fontSize * 2)


game = Game()
