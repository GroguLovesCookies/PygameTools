from components.component import Component
import coordinate.conversions


class DestroyOffscreen(Component):
    def __init__(self, parent, world, screen_size):
        super().__init__(parent)

        self.world = world
        self.screen_size = screen_size


    def tick(self, time):
        aabb = self.parent.shape_AABB
        minX, minY = coordinate.conversions.cartesian_to_pygame(*aabb.min.toarray(), *self.screen_size.toarray())
        maxX, maxY = coordinate.conversions.cartesian_to_pygame(*aabb.max.toarray(), *self.screen_size.toarray())
        if maxX < 0 or minY < 0 or minX > self.screen_size.x or maxY > self.screen_size.y:
            self.world.remove_body(self.parent)