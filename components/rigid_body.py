from components.component import Component
from vector.vector import Vector2


class RigidBodyComponent(Component):
    FPS = 60
    GRAVITY = -9.8/FPS

    COMPONENT_INDEX = 0

    def __init__(self, parent, mass, elasticity):
        super().__init__(parent)

        self.position = self.parent.cartesian_pos
        self.mass = mass
        self.elasticity = elasticity
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

    def tick(self):
        self.acceleration = Vector2(0, RigidBodyComponent.GRAVITY)
        self.velocity += self.acceleration
        self.position += self.velocity

    def trigger_collision(self, collider, other):
        while collider.is_colliding(other):
            self.position -= self.velocity * 0.05
            pos = Vector2(int(self.position.x), int(self.position.y))
            self.parent.set_cartesian_pos(pos)
        self.position -= self.velocity
        self.velocity = Vector2(0, 0)
    
    def late_tick(self):
        pos = Vector2(int(self.position.x), int(self.position.y))
        self.parent.set_cartesian_pos(pos)

