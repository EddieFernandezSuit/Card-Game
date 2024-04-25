import inspect

class Entity:
    def __init__(self, game, *args, **kwargs) -> None:
        self.game = game
        self.__dict__.update(kwargs)
        self.game.currentState['gameObjects'].append(self)
        self.components = []
        # frame = inspect.currentframe()
        # args, _, _, values = inspect.getargvalues(frame)
        # self.__dict__.update(values)
        # print(values)
        self.on_init(*args, **kwargs)
    
    def on_init(self, *args, **kwargs):pass

    def update(self):pass
    
    def delete(self):
        self.on_delete()
        for component in self.components:
            component.delete()
        self.game.currentState['gameObjects'].remove(self)
        del(self)

    def on_delete(self):pass

    def setup(self):pass

    def add_component(self, components):
        for component in components:
            self.components.append(component)
            component.setup()

    def set_component_attribute(self, component):
        temp, end = (component[0], 's') if isinstance(component, list) else (component, '')
        attribute_name = f"{temp.__class__.__name__.lower().replace('component','')}_component" + end
        setattr(self, attribute_name, component)

    def add_components(self, components, list_of_components=None):
        for component in components:
            self.set_component_attribute(component)
        self.add_component(components)

        if list_of_components:
            self.set_component_attribute(list_of_components)
            self.add_component(list_of_components)
