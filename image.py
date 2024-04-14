import pygame
import spritesheet
from classes.aabb import AABB
import json


class Spritesheet:
    def __init__(self, images, file):
        self.images = images
        self.reader = spritesheet.SpritesheetReader(file)
    
    @classmethod
    def sheet_from_json_file(cls, file):
        with open(file, "r+") as f:
            content = json.loads(f.read())
            return cls(content["images"], content["sheetPath"])

    def image_at_pos(self, bounds: AABB):
        return self.reader.image_at((*bounds.min.toarray(), *bounds.size.toarray()), -1)
    
    def image_with_name(self, name: str):
        return self.reader.image_at(self.images[name], -1)



def image_from_file(file):
    return pygame.image.load(file).convert_alpha()
