import pygame
from pygame import transform
import engine
import sys
import random

class GameObject:
    def __init__(self, gameState, components):
        self.components = components
        gameState.objects.append(self)

    def getComp(self, comp):
        for component in self.components:
            if comp == type(component):
                return component
    def removeComp(self, comp):
        for component in self.components:
            if comp == type(component):
                self.components.remove(component)
                return

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
                # GameObject(self.gameState, [TextComp('GameOver',engine.Color.BLACK), PositionComp(600,200)])
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
    def __init__(self, player, state, combatStat):
        self.place = 'hand'
        self.player = player
        self.baseCombatStat = combatStat
        self.level = 1
        self.combatStatText = GameObject(state, [TransformComp(0,0), TextComp(str(combatStat))])
        self.canAttack = 1
        self.manaCost = 1
class BattlefieldComp:
    def __init__(self, playState, createCard):
        def changeStage(self):
            self = self[0]
            if self.stage == 'play':
                self.stage = 'battle'
                stateTextComp.str = 'State: ' + self.stage
            else:
                for x in range(len(self.cardsInBattlefield)):
                    for y in range(len(self.cardsInBattlefield[x])):
                        self.cardsInBattlefield[x][y].getComp(CardComp).canAttack = 1
                self.stage = 'play'
                stateTextComp.str = 'State: ' + self.stage
                self.turn = int(self.turn == 0)
                createCard('delver.png', self.turn, 6)
                turnTextComp.str = 'Player: ' + str(self.turn)
                self.totalMana[self.turn] += 1
                self.mana[self.turn] = self.totalMana[self.turn]

        self.cardsInBattlefield = [[],[]]
        self.hands = [[],[]]
        self.stage = 'play'
        self.turn = 0
        self.selectedCards = []
        self.mana = [1,1]
        self.totalMana = [1,1]

        stateTextComp = TextComp('State: ' + self.stage)
        turnTextComp = TextComp('Player: ' + str(self.turn))
        player1ManaTextComps = TextComp('Mana: ' + str(self.mana[0]))
        player2ManaTextComps = TextComp('Mana: ' + str(self.mana[1]))
        
        self.turnText = GameObject(playState, [TransformComp(1000,200), turnTextComp])
        self.stageText = GameObject(playState, [TransformComp(1000,200 + 25), stateTextComp, ClickableComp(stateTextComp.rect, changeStage, self)])
        self.player1ManaText = GameObject(playState, [TransformComp(1000,200+50), player1ManaTextComps])
        self.player2ManaText = GameObject(playState, [TransformComp(1000,200+75), player2ManaTextComps])

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
        def clickOnCard(card):
            transformComp = card.getComp(TransformComp)
            cardComp = card.getComp(CardComp)
            if cardComp.place == 'field' and battlefieldComp.stage == 'battle':
                if card.getComp(OutlineComp):
                        card.removeComp(OutlineComp)
                        battlefieldComp.selectedCards.remove(card)
                else:
                    if len(battlefieldComp.selectedCards) > 0:
                        def deleteCard(gameState, card):
                            battlefieldComp.cardsInBattlefield[card.getComp(CardComp).player].remove(card)
                            gameState.objects.remove(card.getComp(CardComp).combatStatText)
                            # del card.getComp(CardComp).combatStatText
                            gameState.objects.remove(card)
                            del card

                        def levelUp(card):
                            card.getComp(CardComp).level += 1
                            card.getComp(CardComp).combatStatText.getComp(TextComp).str = str(card.getComp(CardComp).baseCombatStat + card.getComp(CardComp).level)
                            
                        card1CombatStat = int(cardComp.combatStatText.getComp(TextComp).str)
                        card2CombatStat = int(battlefieldComp.selectedCards[0].getComp(CardComp).combatStatText.getComp(TextComp).str)
                        battlefieldComp.selectedCards[0].getComp(CardComp).combatStatText.getComp(TextComp).str = str(int(battlefieldComp.selectedCards[0].getComp(CardComp).combatStatText.getComp(TextComp).str)-card1CombatStat)
                        cardComp.combatStatText.getComp(TextComp).str = str(int(cardComp.combatStatText.getComp(TextComp).str)-card2CombatStat)

                        if int(battlefieldComp.selectedCards[0].getComp(CardComp).combatStatText.getComp(TextComp).str) <= 0:
                            deleteCard(playState, battlefieldComp.selectedCards[0])
                            levelUp(card)

                        if int(cardComp.combatStatText.getComp(TextComp).str) <= 0:
                            deleteCard(playState, card)
                            levelUp(battlefieldComp.selectedCards[0])

                        for selectedCard in battlefieldComp.selectedCards:
                            selectedCard.removeComp(OutlineComp)
                        battlefieldComp.selectedCards = []
                    elif cardComp.canAttack == 1:
                        cardComp.canAttack = 0
                        card.components.append(OutlineComp())
                        battlefieldComp.selectedCards.append(card)
                
            elif battlefieldComp.turn == cardComp.player and cardComp.place == 'hand' and battlefieldComp.stage == 'play' and battlefieldComp.mana[battlefieldComp.turn] - 1 >= 0: 
                battlefieldComp.mana[battlefieldComp.turn] -= 1
                battlefieldComp.hands[battlefieldComp.turn].remove(card)
                if battlefieldComp.turn == 0:
                    transformComp.y += 150
                else:
                    transformComp.y -= 150
                cardComp.place = 'field'
                battlefieldComp.cardsInBattlefield[battlefieldComp.turn].append(card)

        def createCard(imageStr, player, combatStat):
            y = 0
            if player == 0:
                y = 50
            else:
                y = game_.height - 150
                
            card = GameObject(playState, [TransformComp(0,y), ImageComp(imageStr), ClickableComp(pygame.Rect(0,0,100,100), clickOnCard), CardComp(player,playState,combatStat)])
            card.getComp(ClickableComp).args = card
            battlefieldComp.hands[player].append(card)
            
        playState = engine.GameState(game_, 'playState')
        battlefield = GameObject(playState, [BattlefieldComp(playState, createCard)])
        battlefieldComp = battlefield.getComp(BattlefieldComp)
        for i in range(5):
            createCard('delver.png', 0, i+1)
            createCard('delver.png', 1, i+1)
        
    
    menuState = engine.GameState(game_, 'menuState')
    tComp = TextComp('play')
    playText = GameObject(menuState, [TransformComp(300, 300), tComp, ClickableComp(tComp.rect, playAction)])

    menuSelector = [Selector(playText, playAction)]
    GameObject(menuState, [TextSelectorComp(menuSelector)])

def update(game_):
    gameState = game_.gameStates[len(game_.gameStates) - 1]
    events = game_.events
    for object in gameState.objects:
        def drawImage(comps):
            game_.screen.blit(comps[1].image, (comps[0].x, comps[0].y))
        def controlPlayer(comps):
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                comps[0].x -= comps[1].speed
            if keys[pygame.K_RIGHT]:
                comps[0].x += comps[1].speed
            if keys[pygame.K_UP]:
                comps[0].y -= comps[1].speed
            if keys[pygame.K_DOWN]:
                comps[0].y += comps[1].speed
        def drawText(comps):
            # comps[0].textSurface = game_.myFont.render(comps[0].str, True, comps[0].color)
            comps[0].textSurface = comps[0].font.render(comps[0].str, True, comps[0].color)
            game_.screen.blit(comps[0].textSurface, (comps[1].x, comps[1].y))
        def selectText(comps):
            for event in events: #pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        getComponent(comps[0].selectArray[comps[0].selectNum].text, TextComp).color = engine.Color.BLACK
                        comps[0].selectNum += 1
                        if comps[0].selectNum >= len(comps[0].selectArray):
                            comps[0].selectNum = 0
                    if event.key == pygame.K_UP:
                        getComponent(comps[0].selectArray[comps[0].selectNum].text, TextComp).color = engine.Color.BLACK
                        comps[0].selectNum -= 1
                        if comps[0].selectNum < 0:
                            comps[0].selectNum = len(comps[0].selectArray) - 1
                    if event.key == pygame.K_SPACE:
                        comps[0].selectArray[comps[0].selectNum].action()
            getComponent(comps[0].selectArray[comps[0].selectNum].text, TextComp).color = engine.Color.YELLOW
        def updateCreatureStats(obj):
            creatureComp = obj.getComp(CreatureComp)
            if (creatureComp):
                creatureComp.healthText.getComp(TextComp).str = 'Hp: ' + str(creatureComp.health)
                creatureComp.expText.getComp(TextComp).str = 'Exp: ' + str(creatureComp.exp)
                creatureComp.levelText.getComp(TextComp).str = 'Lvl: ' + str(creatureComp.level)
        def updateMove(obj):
            positionComp = obj.getComp(TransformComp)
            movementComp = obj.getComp(MovementComp)
            if positionComp and movementComp:
                positionComp.x += movementComp.dx
                positionComp.y += movementComp.dy
        def updateTimerDelete(gameObject):
            timerDeleteComp = gameObject.getComp(TimerDeleteComp)
            if timerDeleteComp:
                timerDeleteComp.time += 1
                if timerDeleteComp.time == timerDeleteComp.timeEnd:
                    gameState.objects.remove(gameObject)
        def updateClickables(gameObject):
            clickableComp = gameObject.getComp(ClickableComp)
            positionComp = gameObject.getComp(TransformComp)
            if clickableComp and positionComp:
                clickableComp.rect.x = positionComp.x
                clickableComp.rect.y = positionComp.y
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePosition = event.pos
                        if positionComp.rect.collidepoint(mousePosition):
                            if clickableComp.args:
                                clickableComp.action(clickableComp.args)
                            else:
                                clickableComp.action()
        def updateTransform(gameObject):
            transformComp = gameObject.getComp(TransformComp)
            if transformComp:
                transformComp.rect.x = transformComp.x
                transformComp.rect.y = transformComp.y
        def updateCard(gameObject):
            cardComp = gameObject.getComp(CardComp)
            transformComp = gameObject.getComp(TransformComp)
            if cardComp and transformComp:
                textTransformComp = cardComp.combatStatText.getComp(TransformComp)
                textTransformComp.x = transformComp.x
                textTransformComp.y = transformComp.y + 100
        def updateOutline(gameObject):
            outlineComp = gameObject.getComp(OutlineComp)
            transformComp = gameObject.getComp(TransformComp)
            if outlineComp and transformComp:
                pygame.draw.rect(game_.screen, engine.Color.RED, (transformComp.x, transformComp.y, 100,100), 2)
        def updateBattleField(gameObject):
            battlefieldComp = gameObject.getComp(BattlefieldComp)
            if battlefieldComp:
                battlefieldComp.player1ManaText.getComp(TextComp).str = 'Mana: ' + str(battlefieldComp.mana[0])
                battlefieldComp.player2ManaText.getComp(TextComp).str = 'Mana: ' + str(battlefieldComp.mana[1])
                for w in range(len(battlefieldComp.hands)):
                    for x in range(len(battlefieldComp.hands[w])):
                        battlefieldComp.hands[w][x].getComp(TransformComp).x = 150 * x + 50
                for w in range(2):
                    for x in range(len(battlefieldComp.cardsInBattlefield[w])):
                        battlefieldComp.cardsInBattlefield[w][x].getComp(TransformComp).x = 50 + x * 150

        doComp(object, [TransformComp, ImageComp], drawImage)
        doComp(object, [TransformComp, ControlMovementComp], controlPlayer)
        doComp(object, [TextComp, TransformComp], drawText)
        doComp(object, [TextSelectorComp], selectText)
        doComp(object, [CreatureComp], updateCreatureStats)
        
        updateCreatureStats(object)
        updateMove(object)
        updateTimerDelete(object)
        updateClickables(object)
        updateTransform(object)
        updateCard(object)
        updateOutline(object)
        updateBattleField(object)

game = engine.Game(1400, 700, start, update)
