import pygame
import coordinate.conversions


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
    def __init__(self, rect, col, screen_size, anchor = Anchors.CENTER_X|Anchors.CENTER_Y):
        super().__init__()

        self.screen_size = screen_size
        self.anchor = anchor

        self.size = (rect[2], rect[3])
        if type(rect[2]) == float:
            if rect[2] == Anchors.FILL_HORIZONTAL:
                self.size = (self.screen_size[0], rect[3])
        if type(rect[3]) == float:
            if rect[3] == Anchors.FILL_VERTICAL:
                self.size = (rect[2], self.screen_size[1])

        self.pos = coordinate.conversions.cartesian_to_pygame(rect[0], rect[1], *self.screen_size)
        if type(rect[0]) == float:
            self.set_position((
                0 if rect[0] == Anchors.SNAP_TO_LEFT else self.screen_size[0],
                self.pos[1]
            ))
        if type(rect[1]) == float:
            self.set_position((
                self.pos[0],
                0 if rect[1] == Anchors.SNAP_TO_TOP else self.screen_size[1],
            ))
        self.cartesian_pos = (rect[0], rect[1])

        self.surface = pygame.Surface(self.size)
        self.surface.fill(col)
        self.rect = self.surface.get_rect()
        
        self.set_anchor(anchor)

    def set_anchor(self, anchor):
        self.anchor = anchor
        anchor_x = Anchors.MASK_X & self.anchor
        anchor_y = Anchors.MASK_Y & self.anchor

        if anchor_x == Anchors.LEFT_X:
            offset_x = 0
        elif anchor_x == Anchors.CENTER_X:
            offset_x = -self.size[0]//2
        else:
            offset_x = -self.size[0]

        if anchor_y == Anchors.TOP_Y:
            offset_y = 0
        elif anchor_y == Anchors.CENTER_Y:
            offset_y = -self.size[1]//2
        else:
            offset_y = -self.size[1]

        self.rect.left = self.pos[0] + offset_x
        self.rect.top = self.pos[1] + offset_y
        

    def set_position(self, pos):
        self.pos = pos
        self.cartesian_pos = coordinate.conversions.pygame_to_cartesian(*pos, *self.screen_size)
