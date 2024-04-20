from components.component import Component
from components.rigid_body import RigidBodyComponent
from components.polygon_collider import PolygonCollider
from components.animator import Animator
from input_handler import InputHandler
from vector.vector import Vector2
import pygame
from casts import cast_ray


class CharacterController(Component):
    def __init__(self, parent, speed, jump_power, jumps = 1):
        super().__init__(parent)
        self.rb = self.parent.get_component(RigidBodyComponent)
        self.collider = self.parent.get_component(PolygonCollider)
        self.anim = self.parent.get_component(Animator)
        if self.rb is None:
            raise RuntimeError("Rigidbody not present on same sprite as character controller")

        self.speed = speed
        self.jump_power = jump_power

        self.max_jumps = jumps
        self.jumps = jumps

    def tick(self, time):
        self.rb.linear_velocity.x = InputHandler.Instance.get_axis_x() * self.speed
        if self.rb.linear_velocity.x < 0:
            self.parent.flip = False
        elif self.rb.linear_velocity.x > 0:
            self.parent.flip = True
            

        hit = cast_ray(self.parent.cartesian_pos, Vector2(0, -1), self.parent.shape_AABB.size.y//2 + 2, self.collider.colliders, [self.collider])

        if hit:
            self.jumps = self.max_jumps

        if InputHandler.Instance.get_key_down(pygame.K_SPACE) and self.jumps > 0:
            self.rb.add_force(Vector2(0, self.jump_power))
            self.rb.linear_velocity = Vector2(0, 0)
            # self.jumps -= 1


        if self.anim is not None:
            if not hit:
                self.anim.set_state("Jump")
            else:
                self.anim.set_state("Idle" if self.rb.linear_velocity.x == 0 else "Walk")