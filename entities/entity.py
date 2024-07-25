
class Entity:
    def __init__(self, game, *args, **kwargs) -> None:
        self.game = game
        self.game.currentState['gameObjects'].append(self)
        self.components = []
        self.on_init(*args, **kwargs)
    
    def on_init(self, *args, **kwargs):pass

    def set_attributes(self, locals):
        self.__dict__.update(locals)

    def update(self):pass
    
    def delete(self):
        self.on_delete()
        for component in self.components:
            component.delete()
        self.game.currentState['gameObjects'].remove(self)
        del(self)

    def on_delete(self):pass

    def setup(self):pass

    def set_component_attribute(self, component):
        temp, end = (component[0], 's') if isinstance(component, list) else (component, '')
        attribute_name = f"{temp.__class__.__name__.lower().replace('component','')}_component" + end
        setattr(self, attribute_name, component)

    def add_components(self, *args):
        components = []
        for arg in args:
            if isinstance(arg, list):
                self.set_component_attribute(arg)
                components.extend(arg)
            else:
                components.append(arg)

        for component in components:
            self.set_component_attribute(component)
            self.components.append(component)
            component.setup()
    