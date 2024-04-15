from image import Spritesheet
from classes.aabb import AABB
from vector.vector import Vector2
import pygame
import json


class Tile:
    def __init__(self, name, img):
        self.name = name
        self.img = img.convert_alpha()


class TilePalette:
    def __init__(self, tiles):
        self.tiles = tiles

    @classmethod
    def from_json(cls, file):
        with open(file, "r+") as f:
            content = json.loads(f.read())
            all_tiles = []
            for group in content["groups"]:
                group_type = group["type"]
                group_name = group["name"]
                tiles = []
                if group_type == "sheet":
                    sheet = Spritesheet.sheet_from_json_file(group["sheet"])

                    if group["tiles"] == "*":
                        for name, img in sheet.images.items():
                            sprite = sheet.image_at_pos(AABB(Vector2(img[0], img[1]), Vector2(img[0] + img[2], img[1] + img[3])))
                            tiles.append(Tile(name, sprite))
                    else:
                        for tile in group["tiles"]:
                            img = sheet.images[tile["name"]]
                            sprite = sheet.image_at_pos(AABB(Vector2(img[0], img[1]), Vector2(img[0] + img[2], img[1] + img[3])))
                            tiles.append(Tile(tile["name"], sprite))
                
                all_tiles.extend(tiles)
            return cls(all_tiles)

    def add_tile(self, tile):
        self.tiles.append(tile)

    def get_tile(self, tile):
        return self.tiles[tile]