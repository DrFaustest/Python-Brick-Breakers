import math


class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self  # __iadd__ should return self
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        return self
    
    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def __itruediv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        return self
    
    def __neg__(self):
        return Vector2D(-self.x, -self.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    
    def normalize(self):
        magnitude = self.length()
        if magnitude > 0:
            return Vector2D(self.x / magnitude, self.y / magnitude)
        return Vector2D(0, 0)
    
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def set_magnitude(self, new_magnitude):
        normalized = self.normalize()
        self.x = normalized.x * new_magnitude
        self.y = normalized.y * new_magnitude


    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def reflect(self, normal):
        # Reflect this vector on a surface defined by the given normal
        n = normal.normalize()
        return self - n * 2 * self.dot(n)
