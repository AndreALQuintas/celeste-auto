class Macro:
    start: float
    end: float
    action = None
    def __init__(self, start, action, end=None):
        self.start = start
        self.action = action
        self.end = end

    def __str__(self):
        return f"{round(self.start, 3)} - {round(self.end, 3)} - {self.action}\n"

    def __repr__(self):
        return f"{round(self.start, 3)} - {round(self.end, 3)} - {self.action}\n"

    def set_end(self, end: float):
        self.end = end