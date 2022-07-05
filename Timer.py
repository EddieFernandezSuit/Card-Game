
class Timer:
    def __init__(self, time, action) -> None:
        self.time = time
        self.timer = 0
        self.action = action
    
    def update(self):
        self.timer += 1
        if self.timer > self.time:
            self.action()
            del self
