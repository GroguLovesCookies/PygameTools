from components.component import Component
from components.rigid_body import RigidBodyComponent
from vector.vector import Vector2
from classes.chain_function import ChainFunction


class Semisolid(Component):
    def __init__(self, parent, coll, min_dot=0):
        super().__init__(parent)
        self.coll = coll
        self.direction = Vector2(0, 1)
        self.min_dot = min_dot

        self.coll.is_colliding.add_at_head(self.check_can_collide)

    def check_can_collide(self, other):
        dot = other.parent.get_component(RigidBodyComponent).linear_velocity.normalized.dot(self.direction)
        if dot >= self.min_dot or (hasattr(other, "skip_semisolid") and other.skip_semisolid):
            return ChainFunction.END

        return other