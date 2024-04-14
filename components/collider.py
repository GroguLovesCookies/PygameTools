from components.component import Component
from components.rigid_body import RigidBodyComponent
from vector.vector import Vector2


class Collider(Component):
    COMPONENT_INDEX = 1
    Checked = []

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
            if collider.id == self.id:
                continue
            
            boundsA = self.parent.shape_AABB
            boundsB = collider.parent.shape_AABB

            if boundsA.min.x > boundsB.max.x or boundsA.max.x < boundsB.min.x or boundsA.min.y > boundsB.max.y or boundsA.max.y < boundsB.min.y:
                print("Skipping Collision Check")
                continue

            collision = self.is_colliding(collider)
            if collision is not None:
                return *collision, collider

        return None, None, None
    
    def tick(self, time):
        normal, depth, coll = self.check_all_collisions()

        if coll is not None:
            rb1 = self.parent.get_component(RigidBodyComponent)
            rb2 = coll.parent.get_component(RigidBodyComponent)
            first_was_static = False
            second_was_static = False

            if rb1 is None or rb1.static:
                first_was_static = True
            else:
                self.parent.move_cartesian_pos((-normal*0.5)*depth)

            if rb2 is not None and not rb2.static:
                if first_was_static:
                    rb2.parent.move_cartesian_pos(normal*depth)
                else:
                    rb2.parent.move_cartesian_pos(normal*0.5*depth)
            else:
                second_was_static = True

            if second_was_static:
                self.parent.move_cartesian_pos((-normal*0.5)*depth)

            restitution = min(rb1.restitution, rb2.restitution)

            rel_dot_normal = (rb2.linear_velocity - rb1.linear_velocity).dot(normal)
            if rel_dot_normal >= 0:
                return

            j = -(1 + restitution) * rel_dot_normal
            j /= rb1.inv_mass + rb2.inv_mass

            rb1.linear_velocity -= j * rb1.inv_mass * normal
            rb2.linear_velocity += j * rb2.inv_mass * normal

                

    def late_tick(self, time):
        ...