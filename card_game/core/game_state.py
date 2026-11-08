class GameState:
    def __init__(self, game, state_name, create_state=lambda x : 10, **kwargs) -> None:
        self.state_name = state_name
        self.gameObjects = []
        # States that do not need networking (menu, deck builder) keep this as
        # None; process_network must tolerate that.
        self.client = None
        self.__dict__.update(kwargs)
        self.game = game
        self.is_state_created=False
        self.create_state=create_state
        # self.background = Background(game, game_objs=self.gameObjects)
    
    def update_objects(self):
        for gameObject in self.gameObjects:
            gameObject.update()
        
    def create(self):
        self.create_state(self.game)
    
    def set(self, **kwargs):
        self.__dict__.update(kwargs)
        # self.game.set_state('menu')

    def update(self, dict):
        for key in dict:
            setattr(self, key, dict[key])
    
    def send(self, obj):
        self.client.send(obj)
    
    def process_network(self):
        if self.client is not None:
            self.client.process_messages()