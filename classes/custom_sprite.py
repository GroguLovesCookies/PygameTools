import pygame
import coordinate.conversions
from vector.vector import Vector2
from components.component import Component
from typing import List


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
    def __init__(self, pos: Vector2, size: Vector2, col, screen_size: Vector2, anchor = Anchors.CENTER_X|Anchors.CENTER_Y):
        super().__init__()
        self.pos_changed = []

        self.screen_size = screen_size
        self.anchor = anchor

        self.size = size
        if type(size.x) == float:
            if size.x == Anchors.FILL_HORIZONTAL:
                self.size.x = self.screen_size.x
        if type(size.y) == float:
            if size.y == Anchors.FILL_VERTICAL:
                self.size.y = self.screen_size[1]
        
        self.surface = pygame.Surface(self.size.toarray())
        self.surface.fill(col)
        self.rect = self.surface.get_rect()

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

    def set_anchor(self, anchor):
        self.anchor = anchor
        anchor_x = Anchors.MASK_X & self.anchor
        anchor_y = Anchors.MASK_Y & self.anchor

        if anchor_x == Anchors.LEFT_X:
            offset_x = 0
        elif anchor_x == Anchors.CENTER_X:
            offset_x = -self.size.x//2
        else:
            offset_x = -self.size.x

        if anchor_y == Anchors.TOP_Y:
            offset_y = 0
        elif anchor_y == Anchors.CENTER_Y:
            offset_y = -self.size.y//2
        else:
            offset_y = -self.size.y

        self.rect.left = self.pos.x + offset_x
        self.rect.top = self.pos.y + offset_y

    def set_position(self, pos: Vector2):
        self.pos = pos
        self.cartesian_pos = Vector2(*coordinate.conversions.pygame_to_cartesian(*pos.toarray(), *self.screen_size.toarray()))
        self.set_anchor(self.anchor)
        for callback in self.pos_changed:
            callback()

    def set_cartesian_pos(self, pos: Vector2):
        self.cartesian_pos = pos
        self.pos = Vector2(*coordinate.conversions.cartesian_to_pygame(*pos.toarray(), *self.screen_size.toarray()))
        self.set_anchor(self.anchor)
        for callback in self.pos_changed:
            callback()

    def tick(self):
        for component in self.components:
            component.tick()
        for component in self.components:
            component.late_tick()

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
        self.components.insert(i, component)

        return component
            