class Wall:
    def __init__(self, start, end) -> None:
        """
        Initialize a wall line
        :param start: The start position of the wall line
        :param end: The end position of the wall line
        """
        self.start = start
        self.end = end
        self.intersecting = False

    def __repr__(self) -> str:
        """
        Representation magic method
        :return: Returns the representation string
        """
        return f"{str(self.__class__.__name__)}(start={str(self.start)}, end={str(self.end)}, intersecting={str(self.intersecting)})"
