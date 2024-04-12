from components.component import Component
from components.rigid_body import RigidBodyComponent
from vector.vector import Vector2


class Collider(Component):
    COMPONENT_INDEX = 1

    def __init__(self, parent, colliders_to_check, offset: Vector2 = Vector2(0, 0)):
        super().__init__(parent)
        self.colliders = colliders_to_check
        self.offset = offset
        self.center = self.parent.cartesian_pos + self.offset
        self.parent.pos_changed.append(self.on_parent_pos_change)
    
    def on_parent_pos_change(self):
        self.center = self.parent.cartesian_pos + self.offset


    def is_colliding(self, other) -> bool:
        return True

    def check_all_collisions(self) -> bool:
        for collider in self.colliders:
            if self.is_colliding(collider):
                return collider

        return
    
    def tick(self):
        coll = self.check_all_collisions()
        if coll is not None:
            rb = self.parent.get_component(RigidBodyComponent)
            if rb is not None:
                rb.trigger_collision(self, coll)

    def late_tick(self):
        ...