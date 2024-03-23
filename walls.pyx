cdef class Wall:
    cdef tuple start
    cdef tuple end
    cdef bint intersecting

    def __cinit__(self, start, end):
        """
        Initialize a wall line
        :param start: The start position of the wall line
        :param end: The end position of the wall line
        """
        self.start = start
        self.end = end
        self.intersecting = False

    def __repr__(self):
        """
        Representation magic method
        :return: Returns the representation string
        """
        return "{}(start={}, end={}, intersecting={})".format(self.__class__.__name__, str(self.start), str(self.end), str(self.intersecting)).encode('utf-8')
