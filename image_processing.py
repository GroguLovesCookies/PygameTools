import cv2
from image import Spritesheet


def tile_is_empty(bounds, img):
    sliced = img[bounds[0]:bounds[0]+bounds[2], bounds[1]:bounds[1]+bounds[3]]
    for y in range(sliced.shape[0]):
        for x in range(sliced.shape[1]):
            if sliced[y][x][3] > 0:
                return False
    
    return True


def get_empty_tiles(file):
    sheet = Spritesheet.sheet_from_json_file(file)
    img = cv2.imread(sheet.file, cv2.IMREAD_UNCHANGED)
    remove = []
    for tile, bounds in sheet.images.items():
        if tile_is_empty(bounds, img):
            remove.append(tile)

    for tile in remove:
        sheet.images.pop(tile)
    
    sheet.save_to_json(file)

    

get_empty_tiles("images/sheets/stone_sheet.json")