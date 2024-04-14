import pygame
import coordinate.conversions
from vector.vector import Vector2
from components.component import Component
from typing import List
import numpy
from classes.aabb import AABB
from image import *


class Anchors:
    CENTER_X =       0b0000
    LEFT_X =         0b0001
    RIGHT_X =        0b0010
    CENTER_Y =       0b0000
    TOP_Y =          0b0100
    BOTTOM_Y =       0b1000

    SNAP_TO_LEFT =   0.5
    SNAP_TO_RIGHT =  1.5
    SNAP_TO_TOP =    0.5
    SNAP_TO_BOTTOM = 1.5

    FILL_HORIZONTAL = 0.5
    FILL_VERTICAL =   0.5

    MASK_X =         0b0011
    MASK_Y =         0b1100


class CustomSprite(pygame.sprite.Sprite):
    TYPE_CIRCLE = 0
    TYPE_POLYGON = 1
    TYPE_OTHER = 2

    def __init__(self, pos: Vector2, dimensions, col, screen_size: Vector2, anchor = Anchors.CENTER_X|Anchors.CENTER_Y, sprite_type = TYPE_POLYGON, rotation: float = 0):
        super().__init__()
        self.pos_changed = []

        self.screen_size = screen_size
        self.anchor = anchor
        
        self.rotation = numpy.deg2rad(rotation)
        self.sin = numpy.sin(rotation)
        self.cos = numpy.cos(rotation)

        self.col = col
        self.img = None

        self.flip = False

        self.sprite_type = sprite_type
        if self.sprite_type == CustomSprite.TYPE_CIRCLE:
            self.radius = dimensions
        elif self.sprite_type == CustomSprite.TYPE_POLYGON:
            self.vertices = dimensions


        self.set_cartesian_pos(pos)
        if type(pos.x) == float:
            self.set_position(Vector2(
                0 if pos.x == Anchors.SNAP_TO_LEFT else self.screen_size.x,
                self.pos.y
            ))
        if type(pos.y) == float:
            self.set_position(Vector2(
                self.pos.x,
                0 if pos.y == Anchors.SNAP_TO_TOP else self.screen_size.y,
            ))

        self.components: List[Component] = []

    def set_texture(self, texture):
        self.img = texture

    @classmethod
    def create_image_sprite(cls, pos, img, scr_size, rot = 0, anchor = Anchors.CENTER_X|Anchors.CENTER_Y, sheet = None):
        if sheet is None:
            texture = image_from_file(img)
        else:
            texture = sheet.image_with_name(img)

        texture = texture.convert_alpha()

        rect = texture.get_rect()
        size = Vector2(*rect.size)
        
        sprite = CustomSprite.create_rectangular_sprite(pos, size, (0, 0, 0), scr_size, rot, anchor)
        sprite.set_texture(texture)
        sprite.sheet = sheet
        return sprite

    @classmethod
    def create_rectangular_sprite(cls, pos, size, col, scr_size, rot = 0, anchor = Anchors.CENTER_X|Anchors.CENTER_Y):
        vertices = [
            Vector2(-size.x//2, -size.y//2),
            Vector2(-size.x//2, size.y//2),
            Vector2(size.x//2, size.y//2),
            Vector2(size.x//2, -size.y//2)
        ]
        return cls(pos, vertices, col, scr_size, anchor, CustomSprite.TYPE_POLYGON, rot)

    def true_vertices(self, camera):
        if self.sprite_type == CustomSprite.TYPE_POLYGON:
            output = []
            for vert in self.vertices:
                rx = self.cos * vert.x - self.sin * vert.y
                ry = self.sin * vert.x + self.cos * vert.y

                screen_coords = coordinate.conversions.cartesian_to_pygame(rx + self.cartesian_pos.x, ry + self.cartesian_pos.y, *self.screen_size.toarray())
                try:
                    output.append([int(screen_coords[0]) + camera.scroll.x, int(screen_coords[1] + camera.scroll.y)])
                except:
                    output.append((0, 0))
            return output

    @property
    def shape_AABB(self) -> AABB:
        minX = minY = 10000000000000000
        maxX = maxY = -10000000000000000

        if self.sprite_type == CustomSprite.TYPE_CIRCLE:
            minX = self.cartesian_pos.x - self.radius
            maxX = self.cartesian_pos.x + self.radius
            minY = self.cartesian_pos.y - self.radius
            maxY = self.cartesian_pos.y + self.radius
        elif self.sprite_type == CustomSprite.TYPE_POLYGON:
            for vert in self.cartesian_vertices:
                if vert.x < minX:
                    minX = vert.x
                elif vert.x > maxX:
                    maxX = vert.x
                
                if vert.y < minY:
                    minY = vert.y
                if vert.y > maxY:
                    maxY = vert.y


        return AABB(Vector2(minX, minY), Vector2(maxX, maxY))

    @property
    def cartesian_vertices(self):
        if self.sprite_type == CustomSprite.TYPE_POLYGON:
            output = []
            for vert in self.vertices:
                rx = self.cos * vert.x - self.sin * vert.y
                ry = self.sin * vert.x + self.cos * vert.y

                coords = Vector2(rx + self.cartesian_pos.x, ry + self.cartesian_pos.y)
                output.append(coords)
            return output

    @property
    def edge_normals(self):
        normals = []
        for i, vert in enumerate(self.cartesian_vertices):

            next_vert = self.cartesian_vertices[(i+1) % len(self.vertices)]
            edge = next_vert - vert
            normals.append(Vector2(-edge.y, edge.x))
        return normals


    def set_position(self, pos: Vector2):
        self.pos = pos
        self.cartesian_pos = Vector2(*coordinate.conversions.pygame_to_cartesian(*pos.toarray(), *self.screen_size.toarray()))
        for callback in self.pos_changed:
            callback()

    def set_cartesian_pos(self, pos: Vector2):
        self.cartesian_pos = pos
        self.pos = Vector2(*coordinate.conversions.cartesian_to_pygame(*pos.toarray(), *self.screen_size.toarray()))
        for callback in self.pos_changed:
            callback()

    def move_cartesian_pos(self, amount: Vector2):
        self.set_cartesian_pos(self.cartesian_pos + amount)

    def set_rotation(self, rotation):
        self.rotation = numpy.deg2rad(rotation)
        self.sin = numpy.sin(rotation)
        self.cos = numpy.cos(rotation)

    def rotate(self, amount):
        self.set_rotation(numpy.rad2deg(self.rotation) + amount)

    def tick(self, time):
        for component in self.components:
            component.tick(time)
        for component in self.components:
            component.late_tick(time)

    def add_component(self, component_type: type, *args):
        component = component_type(self, *args)
        if len(self.components) == 0:
            self.components.append(component)
            return component

        min_index = 0
        max_index = len(self.components)
        i = (max_index - min_index) // 2
        item = self.components[i]
        while item.COMPONENT_INDEX != component.COMPONENT_INDEX and max_index > min_index:
            if item.COMPONENT_INDEX > component.COMPONENT_INDEX:
                max_index = i
            else:
                min_index = i + 1
            i = (max_index - min_index) // 2
        self.components.insert(i + 1, component)

        return component

    def get_component(self, component_type: type):
        for component in self.components:
            if type(component) == component_type:
                return component
        return
    
    def draw(self, screen, camera):
        true_pos = self.pos + camera.scroll

        if self.img is not None:
            new_img = pygame.transform.rotate(self.img, numpy.rad2deg(self.rotation))
            if self.flip:
                new_img = pygame.transform.flip(new_img, True, False)
            rect = new_img.get_rect()
            rect.center = true_pos.toarray()
            screen.blit(new_img, rect)
        elif self.sprite_type == CustomSprite.TYPE_CIRCLE:
            pygame.draw.circle(screen, self.col, true_pos.toarray(), self.radius)
        else:
            pygame.draw.polygon(screen, self.col, self.true_vertices(camera))