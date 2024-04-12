import numpy


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) == Vector2:
            return Vector2(self.x * other.x, self.y * other.y)
        return Vector2(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def __abs__(self):
        return self.magnitude

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __getitem__(self, item):
        if item > 1:
            raise ValueError("Index out of range.")
        return self.x if item == 0 else self.y

    def toarray(self):
        return self.x, self.y

    def dot(self, other):
        return self.x*other.x + self.y*other.y

    @property
    def sqr_magnitude(self):
        return self.dot(self)

    @property
    def magnitude(self):
        return numpy.sqrt(self.sqr_magnitude)

    @property
    def angle(self):
        return numpy.arctan2(self.y/self.x)

    @property
    def normalized(self):
        return Vector2(self.x/self.magnitude, self.y/self.magnitude)


Vector2.ZERO = Vector2(0, 0)