
class ImageHandler:
    def __init__(self, image, object, screen) -> None:
        self.image = image
        self.object = object
        self.screen = screen
        self.object.handlers.append(self)
    
    def update(self):
        self.draw()

    def draw(self):
        self.screen.blit(self.image, (self.object.x, self.object.y))

    def drawImage(self, game):
        game.screen.blit(self.image, (self.object.x, self.object.y))