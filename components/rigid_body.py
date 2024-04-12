from components.component import Component
from vector.vector import Vector2
import numpy


class RigidBodyComponent(Component):
    FPS = 60
    GRAVITY = -9.8/FPS

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

        self.body_type = body_type
        if body_type == RigidBodyComponent.TYPE_CIRCLE:
            self.radius = dimensions
            self.get_circle_data()
        else:
            self.width, self.height = dimensions
            self.get_box_data()

        self.mass = self.density * self.area

    def get_circle_data(self):
        self.area = numpy.pi * self.radius * self.radius
    
    def get_box_data(self):
        self.area = self.width * self.height
