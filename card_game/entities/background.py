from card_game.entities.entity import Entity
from card_game.components.transform_component import TransformComponent
from card_game.components.image_component import ImageComponent
from card_game.core.paths import asset_path

class Background(Entity):
    def on_init(self) -> None:
        self.add_components(
            TransformComponent(self.game), 
            ImageComponent(self.game, asset_path('images/background.png'), entity=self)
        )