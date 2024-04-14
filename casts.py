from vector.vector import Vector2
from components.collider import Collider
from typing import List


class CastHit:
    def __init__(self, collider: Collider, contact: Vector2):
        self.collider = collider
        self.poc = contact

    def __bool__(self):
        return self.collider is not None


def cast_ray(source: Vector2, direction: Vector2, distance: float, colliders: List[Collider], ignore: List[Collider] = []) -> CastHit:
    for collider in colliders:
        if collider in ignore:
            continue

        if collider.collides_with_line(source, direction, distance):
            return CastHit(collider, Vector2(0, 0))