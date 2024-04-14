from components.component import Component
from components.rigid_body import RigidBodyComponent
from components.polygon_collider import PolygonCollider
from input_handler import InputHandler
from vector.vector import Vector2
import pygame
from casts import cast_ray


class CharacterController(Component):
    def __init__(self, parent, speed, jump_power):
        super().__init__(parent)
        self.rb = self.parent.get_component(RigidBodyComponent)
        self.collider = self.parent.get_component(PolygonCollider)
        if self.rb is None:
            raise RuntimeError("Rigidbody not present on same sprite as character controller")

        self.speed = speed
        self.jump_power = jump_power

    def tick(self, time):
        self.rb.linear_velocity.x = InputHandler.Instance.get_axis_x() * self.speed
        if self.rb.linear_velocity.x < 0:
            self.parent.flip = True
        elif self.rb.linear_velocity.x > 0:
            self.parent.flip = False

        hit = cast_ray(self.parent.cartesian_pos, Vector2(0, -1), self.parent.shape_AABB.size.y//2 + 10, self.collider.colliders, [self.collider])

        if InputHandler.Instance.get_key_down(pygame.K_SPACE) and hit:
            self.rb.add_force(Vector2(0, self.jump_power))