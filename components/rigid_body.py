from components.component import Component
from vector.vector import Vector2
import numpy


class RigidBodyComponent(Component):
    GRAVITY = Vector2(0, -0.2)

    COMPONENT_INDEX = 0

    TYPE_CIRCLE = 0
    TYPE_BOX = 1

    def __init__(self, parent, density, restitution, dimensions, body_type, static):
        super().__init__(parent)

        self.position = self.parent.cartesian_pos
        self.linear_velocity = Vector2(0, 0)
        self.rotation = 0
        self.rotational_velocity = 0

        self.density = density
        self.area = 0
        self.restitution = restitution
        self.static = static

        self.force = Vector2(0, 0)

        self.body_type = body_type
        if body_type == RigidBodyComponent.TYPE_CIRCLE:
            self.radius = dimensions
            self.get_circle_data()
        else:
            self.width, self.height = dimensions.toarray()
            self.get_box_data()

        self.mass = self.density * self.area
        self.inv_mass = 0 if self.static else 1/self.mass

    def get_circle_data(self):
        self.area = numpy.pi * self.radius * self.radius
    
    def get_box_data(self):
        self.area = self.width * self.height

    def tick(self, time):
        if not self.static:
            self.linear_velocity += self.GRAVITY
            self.linear_velocity += (self.force * self.inv_mass)

        self.parent.move_cartesian_pos(self.linear_velocity)
        self.parent.rotate(self.rotational_velocity)

        self.force = Vector2(0, 0)

    def add_force(self, amount):
        self.force = amount
