class Wall:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"{str(self.__class__.__name__)}(start={str(self.start)}, end={str(self.end)})"
