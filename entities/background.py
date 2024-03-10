from entities.entity import Entity
from components.transform_component import TransformComponent
from components.image_component import ImageComponent

class Background(Entity):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.transform_component = TransformComponent(game, (0,0))
        self.image_component = ImageComponent('Images/background.jpg', self)