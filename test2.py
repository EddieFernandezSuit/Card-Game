class Arrow(Entity):
    def on_init(self, origin_object, target_object):
        self.used = 0
        self.origin_object = origin_object
        self.target_object = target_object

        self.arrow_sound = pygame.mixer.Sound('sounds/arrow-impact.mp3')
        
        transform_component = TransformComponent(self.game, self.origin_object.transform_component.rect.center, speed=50)
        image_component = ImageComponent(filePath='Images/arrow.jpg', entity=self)
        
        self.add_components(transform_component, image_component)
        
        self.transform_component.direction = (pygame.Vector2(self.target_object.transform_component.rect.center) - self.transform_component.rect.center).normalize()
        self.image_component.set_rotation(math.degrees(math.atan2(*self.transform_component.direction)) + 180)

    def update(self):
        if(self.transform_component.rect.colliderect(self.target_object.transform_component.rect)):
            if self.used == 0:
                self.target_object.impaledArrows.append(self)
                self.origin_object.deal_damage(self.target_object)
                self.used = 1
                self.transform_component.speed = 0
                self.game.currentState['arrowFlies'] = 0
                self.arrow_sound.play()

    def on_delete(self):
        self.transform_component.delete()
        self.image_component.delete()