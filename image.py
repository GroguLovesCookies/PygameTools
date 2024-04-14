import pygame
import spritesheet
from classes.aabb import AABB
from vector.vector import Vector2
import json


class Spritesheet:
    def __init__(self, images, file):
        self.images = images
        self.file = file
        self.reader = spritesheet.SpritesheetReader(file)
    
    @classmethod
    def sheet_from_json_file(cls, file):
        with open(file, "r+") as f:
            content = json.loads(f.read())
            return cls(content["images"], content["sheetPath"])
    
    @classmethod
    def sheet_from_png(cls, file, tile_size: Vector2, start: Vector2 = Vector2(0, 0), offset: Vector2 = Vector2(0, 0), gap: Vector2 = Vector2(0, 0)):
        sheet = spritesheet.SpritesheetReader(file)
        size = sheet.sheet.get_rect().size
        pos = offset

        tiles_x = size[0]//(tile_size+gap).x
        tiles_y = size[1]//(tile_size+gap).y

        images = {}

        i = 0
        for y in range(tiles_y):
            pos_y = (tile_size+gap).y * y
            for x in range(tiles_x):
                pos_x = (tile_size+gap).x * x

                images[str(i)] = (pos_x, pos_y, *tile_size.toarray())

                i += 1

        return cls(images, file)

    def save_to_json(self, file):
        with open(file, "w") as f:
            f.write(json.dumps({
                "sheetPath": self.file,
                "images": self.images
            }))

    def image_at_pos(self, bounds: AABB):
        return self.reader.image_at((*bounds.min.toarray(), *bounds.size.toarray()), -1)
    
    def image_with_name(self, name: str):
        return self.reader.image_at(self.images[name], -1)


def image_from_file(file):
    return pygame.image.load(file).convert_alpha()
