from winreg import DisableReflectionKey
from GameObject import GameObject

class TransformHandler(GameObject):
    def __init__(self, game, position) -> None:
        super().__init__(game)
        self.position = position
        self.speed = 0
        self.direction = 0
        self.gravity = 0
        self.vSpeed = 0

    def update(self):
        self.position += self.direction * self.speed
        self.vSpeed += self.gravity
        self.position.y += self.vSpeed
        