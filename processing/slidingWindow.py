import numpy as np

class SlidingWindow():
    def __init__(self, size: int, step: int):
        self.size = size
        self.step = step
        self.window = np.array([])

    def add(self, value):
        self.window = np.append(self.window, value)
        if len(self.window) > self.size:
            self.window = np.delete(self.window, 0)
    
    def get_Average(self):
        return np.average(self.window)