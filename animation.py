import json
from image import Spritesheet, image_from_file


class Keyframe:
    def __init__(self, time, image, sheet = None):
        self.time = time
        self.image = image
        self.sheet = sheet

class Animation:
    def __init__(self, keyframes):
        self.keyframes = keyframes

    @classmethod
    def sheet_animation_from_json(cls, file):
        with open(file, "r+") as f:
            keyframes = []
            content = json.loads(f.read())
            sheet = Spritesheet.sheet_from_json_file(content["sheet"])

            for frame in content["keyframes"]:
                keyframes.append(Keyframe(frame["time"], frame["image"], sheet))

        return cls(keyframes)

    @property
    def length(self):
        max_time = -1
        for keyframe in self.keyframes:
            if keyframe.time > max_time:
                max_time = keyframe.time
        return max_time
    
    def get_image_at_frame(self, frame):
        true_frame = frame % (self.length + 1)

        smallest_distance = 1000000000000000000000000
        closest_keyframe = None
        for keyframe in self.keyframes:
            if keyframe.time <= true_frame:
                distance = true_frame - keyframe.time
                if distance < smallest_distance:
                    smallest_distance = distance
                    closest_keyframe = keyframe

        if closest_keyframe.sheet is None:
            return image_from_file(closest_keyframe.image)
        return closest_keyframe.sheet.image_with_name(closest_keyframe.image)