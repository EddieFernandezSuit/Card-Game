from GameObject import GameObject
import pygame
class ImageHandler(GameObject):
    def __init__(self, filePath, position, game) -> None:
        super().__init__(game)
        self.image = pygame.image.load(filePath).convert_alpha()
        self.screen = game.screen
        self.position = position
        self.angle = 0
    
    def update(self):
        self.draw()

    def draw(self):
        self.screen.blit(self.image, (self.position))
        
    def setAngle(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, self.angle)

    def getCenter(self):
        return pygame.Vector2(self.position.x + self.image.get_rect().width/2, self.position.y + self.image.get_rect().height/2)

    def getRect(self):
        rect = self.image.get_rect()
        rect.x = self.position.x
        rect.y = self.position.y
        return rect

def positionCenter(position, rect):
    return pygame.Vector2(position.x + rect.width/2, position.y + rect.height/2)