"""
Color Label data
"""
#from dataclasses import dataclass

__all__ = ('ColorLabel', )


#@dataclass
class ColorLabel:
    """
    Class for keeping track of a color label
    """
    #name: str
    #min_range: tuple = (0, 0, 0)
    #max_range: tuple = (180, 255, 255)
    #dilate_iterations: int = 2

    __slots__ = ('name', 'min_range', 'max_range', 'dilate_iterations')

    def __init__(self,
                 name,
                 min_range=(0, 0, 0),
                 max_range=(180, 255, 255),
                 dilate_iterations=2):
        self.name = name
        self.min_range = min_range
        self.max_range = max_range
        self.dilate_iterations = dilate_iterations

    def to_tuple(self):
        """Serialize"""
        serialize = []

        for v in self.min_range:
            serialize.append(v)

        for v in self.max_range:
            serialize.append(v)

        serialize.append(self.dilate_iterations)
        return tuple(serialize)

        #return *self.min_range, *self.max_range, self.dilate_iterations

    def from_tuple(self, raw: tuple):
        """De-serialize"""
        self.min_range = raw[:3]
        self.max_range = raw[3:6]
        self.dilate_iterations = raw[-1]
