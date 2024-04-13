class AABB:
    def __init__(self, min_, max_):
        self.min = min_
        self.max = max_

    @property
    def size(self):
        return self.max - self.min