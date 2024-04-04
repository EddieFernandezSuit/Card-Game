from entities.entity import Entity
from components.transform_component import TransformComponent
from components.image_component import ImageComponent

class Background(Entity):
    def on_init(self) -> None:
        self.add_components(
            [TransformComponent(self.game), 
            ImageComponent('Images/background.jpg', entity=self)]
        )