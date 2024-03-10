import math
from entities.entity import Entity
from components.image_component import ImageComponent
from components.transform_component import TransformComponent

class Arrow(Entity):
    def __init__(self, game, originObject, target_object):
        super().__init__(game)
        self.used = 0
        self.object_to_damage = target_object
        self.target_object = target_object
        self.originObject = originObject
        if (type(originObject) != type(target_object)):
            self.target_object = target_object.healthText
        
        self.transform_component = TransformComponent(self.game, self.originObject.transform_component.rect.center)
        self.imageHandler = ImageComponent('Images/arrow.jpg', self)
        self.transform_component.speed = 50
        self.transform_component.direction.x = self.target_object.transform_component.rect.center[0] - self.transform_component.rect.center[0]
        self.transform_component.direction.y = self.target_object.transform_component.rect.center[1] - self.transform_component.rect.center[1]
        self.transform_component.direction = self.transform_component.direction.normalize()

        self.imageHandler.setAngle(math.degrees(math.atan2(self.transform_component.direction.x, self.transform_component.direction.y)) + 180)

    def update(self):
        if(self.transform_component.rect.colliderect(self.target_object.transform_component.rect)):
            if self.used == 0:
                self.object_to_damage.impaledArrows.append(self)
                self.originObject.dealDamage(self.object_to_damage)
                self.used = 1
                self.transform_component.speed = 0
                self.game.currentState['arrowFlies'] = 0

    def delete(self):
        self.game.currentState["arrowFlies"] = 0
        self.game.currentState['gameObjects'].remove(self)
        self.game.currentState["gameObjects"].remove(self.transform_component)
        self.game.currentState['gameObjects'].remove(self.imageHandler)