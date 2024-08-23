

class ThreadManager:
    def __init__(self, action=None) -> None:
        self.kwargs = []
        self.action = []
        if action:
            self.action.append(action)

    def update(self):
        if len(self.action) > 0:
            self.action[0](*self.kwargs[0])
            self.action.pop(0)
            self.kwargs.pop(0)

    def do(self, action, *kwargs):
        self.action.append(action)
        self.kwargs.append(kwargs)