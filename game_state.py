
from typing import Any

from entities.background import Background


class GameState:
    def __init__(self, game, state_name, create_state=lambda x : 10, **kwargs) -> None:
        self.state_name = state_name
        self.gameObjects = []
        self.__dict__.update(kwargs)
        self.game = game
        self.is_state_created=False
        self.create_state=create_state
        # self.background = Background(game, game_objs=self.gameObjects)
    
    def create(self):
        self.create_state(self.game)
    
    def set(self, **kwargs):
        print(kwargs)
        self.__dict__.update(kwargs)
        # self.game.set_state('menu')
    
    def __getitem__(self, key):
        key = str(key)
        # print(self, key)
        if hasattr(self, key):
            return getattr(self, key)
    
    def __setitem__(self, key, new_value):
        setattr(self, key, new_value)
    
    def __contains__(self, item):
        return getattr(self, item, None) != None

    def update(self, dict):
        for key in dict:
            setattr(self, key, dict[key])
    
    def __and__(self, item):
        a = getattr(self, item, Anything())
        print(a)
        return a
    

class Anything:
    def __init__(self) -> None:
        pass

    def __getattr__(self, name):
        def method(*args, **kwargs):
            # Do nothing if method is not found
            pass
        return method