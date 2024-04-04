from components.collider import Collider
from vector.vector import Vector2
import coordinate.conversions


class CircleCollider(Collider):
    def __init__(self, parent, colliders_to_check, size, offset: Vector2 = Vector2(0, 0)):
        super().__init__(parent, colliders_to_check, offset)
        self.size = size

    def is_colliding(self, other):
        if type(other) == CircleCollider:
            total_length = self.size + other.size
            center_diff = (other.center - self.center).sqr_magnitude
            if total_length * total_length > center_diff:
                return True

        return False
