from classes.custom_sprite import CustomSprite
from vector.vector import Vector2


class World:
    def __init__(self):
        self.gravity = Vector2(0, 9.81)
        self.bodies = []


    def add_body(self, body):
        self.bodies.append(body)

    def remove_body(self, body):
        self.bodies.remove(body)

    def tick(self, time):
        for body in self.bodies:
            body.tick(time)

        