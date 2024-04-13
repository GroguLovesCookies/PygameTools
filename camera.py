from classes.aabb import AABB
from vector.vector import Vector2


class Camera:
    def __init__(self, scroll, bounds, screen_size):
        self.scroll = scroll
        self.bounds = bounds
        self.screen_size = screen_size

    def move_to(self, pos, smoothing):
        target = -pos + (self.screen_size * 0.5)
        self.scroll += (target - self.scroll)/smoothing
        if self.bounds is None:
            return

        if self.scroll.x < self.bounds.min.x:
            self.scroll.x = self.bounds.min.x
        elif self.scroll.x > self.bounds.max.x:
            self.scroll.x = self.bounds.max.x
        if self.scroll.y < self.bounds.min.y:
            self.scroll.y = self.bounds.min.y
        elif self.scroll.y > self.bounds.max.y:
            self.scroll.y = self.bounds.max.y
