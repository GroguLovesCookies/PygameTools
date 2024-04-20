import pygame
from classes.custom_sprite import CustomSprite
from vector.vector import Vector2


class Tilemap(CustomSprite):
    def __init__(self, pos, map_data, tile_size, tile_palette, screen_size):
        self.pos = pos
        self.map = map_data
        self.tile_size = tile_size
        self.palette = tile_palette
        self.screen_size = screen_size
        self.tiles = []
        self.components = []
        self.surf = pygame.surface.Surface(self.screen_size.toarray(), pygame.SRCALPHA)
        
        self.block_coords = []
        self.coords_update_needed = True

    def get_block_coords(self):
        if not self.coords_update_needed:
            return self.block_coords

        self.block_coords.clear()
        for y in range(self.size.y):
            for x in range(self.size.x):
                if self.map[y][x] > -1:
                    self.block_coords.append(Vector2(x, y))

        self.coords_update_needed = False
        return self.block_coords

    @property
    def size(self):
        return Vector2(len(self.map[0]), len(self.map))
    
    def draw(self, screen, camera):
        self.surf.fill((0, 0, 0, 0))
        for row_no in range(self.size.y):
            row = self.map[row_no]
            start = int(-(camera.scroll.x+self.pos.x)//self.tile_size.x)
            for tile_no in range(max(start, 0), self.size.x):
                tile_type = row[tile_no]
                if tile_type == -1:
                    continue

                tile = self.palette.get_tile(tile_type)
                
                pos = Vector2(tile_no, row_no) * self.tile_size
                true_pos = pos + self.pos + camera.scroll
                if true_pos.x - self.tile_size.x > self.screen_size.x:
                    break
                if true_pos.x + self.tile_size.x*2 < 0:
                    continue

                self.surf.blit(tile.img, true_pos.toarray())

        screen.blit(self.surf, (0, 0))
    