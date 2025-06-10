class Timer:
    def __init__(self, time, action) -> None:
        self.time = time
        self.timer = 0
        self.action = action
    
    def update(self):
        self.timer += 1
        if self.timer > self.time:
            self.action()
            # self = None
            del self

# import threading

# class Timer:
#     def __init__(self, time, action):
#         self.time = time
#         self.timer = 0
#         self.action = action
#         threading.Thread(target=self.thread, args=()).start()
    
#     def update(self):
#         pass

#     def thread(self):
#         while self.timer < self.time:
#             self.timer += .000001
#         self.action()