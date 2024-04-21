from components.component import Component
from components.rigid_body import RigidBodyComponent
from components.collider import ColliderGroup
from components.polygon_collider import PolygonCollider
from classes.aabb import AABB
from vector.vector import Vector2
from classes.custom_sprite import CustomSprite
from coordinate.conversions import *


class TilemapCollider(Component):
    def __init__(self, parent, colliders, camera, screen_size, screen):
        self.id = -1
        self.parent = parent
        self.colliders = colliders
        self.camera = camera
        self.sprites = []
        self.screen_size = screen_size
        self.screen = screen
        self.groups = []
        self.colliders_created = []


    def is_colliding(self, other):
        screen_AABB = other.parent.screen_AABB(self.camera)
        other_min_pos = screen_AABB.min
        other_max_pos = screen_AABB.max

        other_min_pos -= self.camera.scroll
        other_max_pos -= self.camera.scroll

        other_min_pos -= self.parent.pos
        other_max_pos -= self.parent.pos

        other_min_pos = other_min_pos/self.parent.tile_size
        other_max_pos = other_max_pos/self.parent.tile_size

        other_min_pos = Vector2(int(other_min_pos.x), int(other_min_pos.y))
        other_max_pos = Vector2(int(other_max_pos.x), int(other_max_pos.y))

        
        true_min = Vector2(max(other_min_pos.x - 1, 0), max(other_min_pos.y - 1, 0))
        true_max = Vector2(min(other_max_pos.x + 1, self.parent.size.x), min(other_max_pos.y + 1, self.parent.size.y))
        self.get_vertices(AABB(true_min, true_max), other)


    def get_vertices(self, bounds, collider):
        if bounds.min.y >= bounds.max.y or bounds.min.x >= bounds.max.x:
            return

        for y in range(bounds.min.y, bounds.max.y):
            for x in range(bounds.min.x, bounds.max.x):
                if self.parent.map[y][x] == -1:
                    continue

                pos = Vector2(x+0.5, y+0.5) * self.parent.tile_size
                pos += self.parent.pos
                pos = Vector2(*pygame_to_cartesian(*pos.toarray(), *self.screen_size.toarray())) 
                pos = Vector2(int(pos.x), int(pos.y))
                
                sprite = CustomSprite.create_rectangular_sprite(pos, self.parent.tile_size, (100, 0, 0), self.screen_size)
                sprite.visible = False
                sprite.add_component(RigidBodyComponent, 2, 0.7, Vector2(800, 40), RigidBodyComponent.TYPE_BOX, True)
                coll = sprite.add_component(PolygonCollider, [collider])
                for group in self.groups:
                    ColliderGroup.add_collider_to_group(group, coll)

                self.colliders_created.append(coll)
                self.sprites.append(sprite)
                

    def check_all_collisions(self):
        for collider in self.colliders:
            if collider.id == self.id:
                continue
            self.is_colliding(collider)

        return None, None, None

    def tick(self, time):
        for group in self.groups:
            for coll in self.colliders_created:
                ColliderGroup.remove_collider_from_group(group, coll)
        self.sprites.clear()
        self.check_all_collisions()
        for sprite in self.sprites:
            sprite.tick(time)
            sprite.draw(self.screen, self.camera)

    def collides_with_line(self, source, direction, distance):
        return False

    @property
    def shape_AABB(self):
        return
