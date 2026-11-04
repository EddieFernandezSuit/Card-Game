from entities.entity import Entity
from components.transform_component import TransformComponent
from components.image_component import ImageComponent
from paths import asset_path

class Background(Entity):
    def on_init(self) -> None:
        self.add_components(
            TransformComponent(self.game), 
            ImageComponent(self.game, asset_path('images/background.png'), entity=self)
        )