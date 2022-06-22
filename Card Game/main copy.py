import pygame
from pygame import transform
from pygame import color
import engine
import sys
import random

print('copy')


class ooo:
    def __init__(self):
        self.x = 1
        
    def hasattr(self, attr):
        return hasattr(self, attr)

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)


class GameObject:
    def __init__(self, gameState, attr):
        gameState.objects.append(self)
        for x in range(0, len(attr), 2):
            self[attr[x]] = attr[x+1]
    
    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def hasattr(self, attr):
        return hasattr(self, attr)


class TransformComp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
class ImageComp:
    def __init__(self, image):
        self.image = pygame.image.load(image)
class ControlMovementComp:
    def __init__(self, speed):
        self.speed = speed
class TextComp:
    def __init__(self, str):
        self.str = str
        self.color = engine.Color.BLACK
        self.font = pygame.font.SysFont("arial", 25)
        self.textSurface = self.font.render(self.str, True, self.color)
        self.rect = pygame.Rect(0,0,self.textSurface.get_width(), self.textSurface.get_height())
class TimerDeleteComp:
    def __init__(self, damage, name, bleedDamage, recoilDamage):
        self.damage = damage
        self.name = name
        self.bleedDamage = bleedDamage
        self.recoilDamage = recoilDamage
class CreatureComp:
    def __init__(self, gameState, x, y, name, enemyCreature, isPlayer, level):
        distance = 25
        self.x = x
        self.y = y
        self.isPlayer = isPlayer
        self.health = 100
        self.level = level
        self.exp = 0
        self.bleedDamage = 0
        self.enemyCreature = enemyCreature
        self.gameState = gameState
        self.nameText = GameObject(gameState, [TextComp('Name: ' + name, engine.Color.BLACK), TransformComp(x, y)])
        self.healthText = GameObject(gameState,
                                    [TextComp(str(self.health), engine.Color.BLACK), TransformComp(x, y + distance)])
        self.levelText = GameObject(gameState,
                                    [TextComp(str(self.level), engine.Color.BLACK), TransformComp(x, y + distance * 2)])
        self.expText = GameObject(gameState,
                                    [TextComp(str(self.exp), engine.Color.BLACK), TransformComp(x, y + distance * 3)])
        self.moves = []
        for i in range(self.level):
            self.moves.append(Move(self.moveAction, i,self))

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def changeStat(self, creatureComp, stat, add):
        flyingNumDx = 2
        flyingNumDy = random.uniform(-1, 1)
        flyingNumTime = 70
        if add != 0:
            color = engine.Color.RED
            plus = ''
            if add > 0:
                color = engine.Color.GREEN
                plus = '+'
            creatureComp[stat] = creatureComp[stat] + add
            GameObject(self.gameState, [TransformComp(creatureComp[stat + 'Text'].getComp(TransformComp).x + 30,
                                                    creatureComp[stat + 'Text'].getComp(TransformComp).y),
                                        TextComp(plus + str(add), color), MovementComp(flyingNumDx, flyingNumDy),
                                        TimerDeleteComp(flyingNumTime)])

    def moveAction(self, damage, bleedDamage, recoilDamage):
        self.enemyCreature.getComp(CreatureComp).bleedDamage += bleedDamage
        self.changeStat(self, 'health', self.bleedDamage * -1)
        self.changeStat(self.enemyCreature.getComp(CreatureComp), 'health', damage * -1)
        self.changeStat(self, 'health', recoilDamage * -1)

        if self.isPlayer:
            random.choice(self.enemyCreature.getComp(CreatureComp).moves).action()
            if self.enemyCreature.getComp(CreatureComp).health <= 0:
                playerCreature = self.enemyCreature.getComp(CreatureComp).enemyCreature
                self.gameState.objects.remove(self.enemyCreature.getComp(CreatureComp).nameText)
                self.gameState.objects.remove(self.enemyCreature.getComp(CreatureComp).healthText)
                self.gameState.objects.remove(self.enemyCreature.getComp(CreatureComp).expText)
                self.gameState.objects.remove(self.enemyCreature.getComp(CreatureComp).levelText)
                for x in self.enemyCreature.getComp(CreatureComp).moves:
                    self.gameState.objects.remove(x.text)
                self.gameState.objects.remove(self.enemyCreature)
                self.enemyCreature = GameObject(self.gameState,
                                                [TransformComp(1000, 100), ImageComp('teethBlob.png'),
                                                CreatureComp(self.gameState, 1000, 400, "Bob", playerCreature, False,1)])

                self.changeStat(self, 'exp', 100)
                maxExp = 100
                if self.exp >= maxExp:
                    self.changeStat(self, 'exp', -100)
                    self.changeStat(self, 'level', 1)
                    self.changeStat(self, 'health', 100 - self.health)
                    if self.level == 2:
                        self.moves.append(Move(self.moveAction, 1, self))

            if self.health <= 0:
                # gameObject(self.gameState, [TextComp('GameOver',engine.Color.BLACK), PositionComp(600,200)])
                # self.gameState.game.pause = 1
                self.gameState.game.gameStates.pop()
                start(self.gameState.game)
class TextSelectorComp:
    def __init__(self, selectArray):
        self.selectArray = selectArray
        self.selectNum = 0
class MovementComp:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
class ClickableComp:
    def __init__(self, rect, action, *args):
        self.action = action
        self.args = args
        self.rect = rect
class CardComp:
    def __init__(self, player, state, ):
        self.place = 'hand'
        self.player = player
        self.text = GameObject(state, [TransformComp(0,0), TextComp('1')])
class BattlefieldComp:
    
    def __init__(self, playState):
        def clickOnStage(self):
            self = self[0]
            if self.stage == 'play':
                self.stage = 'battle'
                tComp.str = 'State: ' + self.stage
            else:
                self.stage = 'play'
                tComp.str = 'State: ' + self.stage
                self.turn = int(self.turn == 0)
                turnTextComp.str = 'Player: ' + str(self.turn)

        self.playerZones = [['empty','empty','empty','empty','empty'],['empty','empty','empty','empty','empty']]
        self.stage = 'play'
        self.turn = 0
        tComp = TextComp('State: ' + self.stage)
        turnTextComp = TextComp('Player: ' + str(self.turn))

        self.turnText = GameObject(playState, [TransformComp(1000,200), turnTextComp])
        self.stageText = GameObject(playState, [TransformComp(1000,200 + 25), tComp, ClickableComp(tComp.rect, clickOnStage, self)])
        
    
class OutlineComp:
    def __init__(self):
        self.rect = pygame.Rect(0,0,0,0)

class Selector:
    def __init__(self, text, action):
        self.text = text
        self.action = action
class Move:
    def __init__(self, timeEnd):
        self.time = 0
        self.timeEnd = timeEnd
class unlearnedMove:
    def __init__(self, genericAction, num, creatureComp):
        distance = 25
        unlearnedMoves = [unlearnedMove(10, 'tap', 0, 0), unlearnedMove(0, 'stomp', 5, 0),
                        unlearnedMove(30, 'wack', 0, 10)]
        self.damage = unlearnedMoves[num].damage
        self.bleedDamage = unlearnedMoves[num].bleedDamage
        self.recoilDamage = unlearnedMoves[num].recoilDamage
        self.name = unlearnedMoves[num].name
        self.text = GameObject(creatureComp.gameState,
                            [TextComp(unlearnedMoves[num].name, engine.Color.BLACK),
                                TransformComp(creatureComp.x, creatureComp.y + distance * (5 + num))])
        self.genericAction = genericAction

    def action(self):
        self.genericAction(self.damage, self.bleedDamage, self.recoilDamage)

def getComponent(gameObject, comp):
    for component in gameObject.components:
        if comp == type(component):
            return component
    return None
def doComp(gameObject, compClasses, do):
    comps = []
    for comp in compClasses:
        if gameObject.getComp(comp):
            comps.append(gameObject.getComp(comp))

    if len(comps) == len(compClasses):
        do(comps)

def start(game_):
    def playAction():

        def clickOnStage(self):
            self = self[0]
            if self.stage == 'play':
                self.stage = 'battle'
            else:
                self.stage = 'play'
                self.turn = int(self.turn == 0)
                self.turnText.str = 'Player: ' + str(self.turn)
            
            self.stageText.str = 'State: ' + self.stage
        
        playState = engine.GameState(game_, 'playState')
        battlefield = GameObject(playState, ['playerZones', [['empty','empty','empty','empty','empty'],['empty','empty','empty','empty','empty']], 'stage', 'play', 'turn', 0])
        battlefield.turnText = GameObject(playState, [])
        battlefield.turnText.x = 1000
        battlefield.turnText.y = 200
        battlefield.turnText.str = 'Player: ' + str(battlefield.turn)
        battlefield.stageText = GameObject(playState, [])
        battlefield.stageText.x = 1000
        battlefield.stageText.y = 200 + 25
        battlefield.stageText.str = 'State: ' + battlefield.stage
        battlefield.stageText.color = engine.Color.BLACK
        battlefield.stageText.action = clickOnStage
        battlefield.stageText.args = battlefield

        for i in range(5):
            def clickOnCard(object):
                def getEmptyZone(self, player):
                    for x in range(len(self.playerZones[player])):
                        if self.playerZones[player][x] == 'empty':
                            return x

                if battlefield.turn == object.player:
                    if object.place == 'hand' and battlefield.stage == 'play':
                        zoneIndex = getEmptyZone(battlefield, object.player)
                        print(zoneIndex)
                        if object.player == 0:
                            object.y += 150
                        elif object.player == 1:
                            object.y -= 150
                        object.x = 50 + zoneIndex * 150
                        object.place = 'field'
                        battlefield.playerZones[object.player][zoneIndex] = 'full'

                    elif object.place == 'field' and battlefield.stage == 'battle':
                        if object.outline:
                            object.outline =1
                        else:
                            object.outline = 0

            card = GameObject(playState, ['x', 50 + i * 150, 'y', 50, 'image', pygame.image.load('delver.png'), 'rect', pygame.Rect(0,0,100,100),'action', clickOnCard, 'place', 'hand', 'player', 0])
            card.text = GameObject(playState, ['x', 0, 'y', 0, 'str', '1', 'color', engine.Color.BLACK])
            card.args = card

            # card = GameObject(playState, [TransformComp(50 + i * 150,50), ImageComp('delver.png'), ClickableComp(pygame.Rect(0,0,100,100), clickOnCard), CardComp(0,playState)])
            # card.getComp(ClickableComp).args = card
            # card = GameObject(playState, [TransformComp(50 + i * 150, game_.height - 150), ImageComp('delver.png'), ClickableComp(pygame.Rect(0,0,100,100),clickOnCard), CardComp(1, playState)])
            # card.getComp(ClickableComp).args = card

            card = GameObject(playState, ['x', 50 + i * 150, 'y', game_.height - 150, 'image', pygame.image.load('delver.png'), 'rect', pygame.Rect(0,0,100,100),'action', clickOnCard, 'place', 'hand', 'player', 1])
            card.text = GameObject(playState, ['x', 0, 'y', 0, 'str', '1', 'color', engine.Color.BLACK])
            card.args = card
        
    menuState = engine.GameState(game_, 'menuState')

    playText = GameObject(menuState, ['x', 300, 'y', 300, 'str', 'play', 'color', engine.Color.BLACK, 'action', playAction])

    # playText.x = 300
    # playText.y = 300
    # playText.str = 'play'
    # playText.color = engine.Color.BLACK
    # playText.action = playAction

    menuSelector = [Selector(playText, playAction)]
    MS = GameObject(menuState, ['selectArray', menuSelector, 'selectNum', 0])

def update(game_):
    gameState = game_.gameStates[len(game_.gameStates) - 1]
    events = game_.events
    for object in gameState.objects:
        def drawImage(object):
            if object['image'] and object['x'] and object['y']: 
                game_.screen.blit(object['image'], (object['x'], object['y']))
        def controlPlayer(object):
            if object['speed'] and object['x'] and object['y']:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    object['x'] -= object['speed']
                if keys[pygame.K_RIGHT]:
                    object['x'] += object['speed']
                if keys[pygame.K_UP]:
                    object['y'] -= object['speed']
                if keys[pygame.K_DOWN]:
                    object['y'] += object['speed']
        def drawText(object):
            if object['str'] and object['color'] and object['x'] and object['y']:
                # object['textSurface'] = game_.myFont.render(object['str'], True, object['color'])
                object['font'] = pygame.font.SysFont("arial", 25)
                object['textSurface'] = object['font'].render(object['str'], True, object['color'])
                object['rect'] = pygame.Rect(object['x'], object['y'] ,object['textSurface'].get_width(), object['textSurface'].get_height())
                game_.screen.blit(object['textSurface'], (object['x'], object['y']))
        def selectText(object):
            if object['selectNum'] and object['selectArray'] and object['color']:
                for event in events: #pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            object['selectNum'] += 1
                            if object['selectNum'] >= len(object['selectArray']):
                                object['selectNum'] = 0
                        if event.key == pygame.K_UP:
                            object['selectNum'] -= 1
                            if object['selectNum'] < 0:
                                object['selectNum'] = len(object['selectArray']) - 1
                        if event.key == pygame.K_SPACE:
                            object['selectArray'][object['selectNum']].action()
                object['color'] = engine.Color.YELLOW
        def updateMove(obj):
            if obj['x'] and obj['y'] and obj['dx'] and obj['dy']:
                    obj['x'] += obj['dx']
                    obj['y'] += obj['dy']
        def updateTimerDelete(gameObject):
            if gameObject['time']:
                gameObject['time'] += 1
                if gameObject['time'] == gameObject['time']:
                    gameState.objects.remove(gameObject)
        def updateClickables(gameObject):
            if gameObject['rect'] and gameObject['x'] and gameObject['action']:
                gameObject['rect'].x = gameObject['x']
                gameObject['rect'].y = gameObject['y']
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePosition = event.pos
                        if gameObject['rect'].collidepoint(mousePosition):
                            if gameObject['args']:
                                gameObject.action(gameObject['args'])
                            else: 
                                gameObject.action()

        def updateCard(gameObject):
            if gameObject['x'] and gameObject['text']:
                gameObject['text'].x = gameObject['x']
                gameObject['text'].y = gameObject['y'] + 100
        def updateOutline(gameObject):
            if gameObject['x'] and gameObject['outline']:
                pygame.draw.rect(game_.screen, engine.Color.RED, (gameObject['x'], gameObject['y'], 100,100), 2)

        drawImage(object)
        controlPlayer(object)
        drawText(object)
        selectText(object)
        updateMove(object)
        updateTimerDelete(object)
        updateClickables(object)
        updateCard(object)
        updateOutline(object)

game = engine.Game(1400, 700, start, update)
