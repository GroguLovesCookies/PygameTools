from components.component import Component
from animation import Animation
import json


class Animator(Component):
    def __init__(self, parent, animations, default_state):
        super().__init__(parent)
        self.animations = animations
        self.current_state = default_state
        self.speed = 1
        self.frame = 0

    def state_animation(self, state):
        return self.animations[state]

    def tick(self, time):
        cur_anim = self.state_animation(self.current_state)
        
        img = cur_anim.get_image_at_frame(self.frame)
        self.parent.set_texture(img)

        self.frame += 1

    def set_state(self, state):
        if state not in self.animations.keys() or state == self.current_state:
            return
        self.current_state = state
        self.frame = 0

    @classmethod
    def from_json(cls, parent, file):
        with open(file, "r+") as f:
            animations = {}
            content = json.loads(f.read())
            for animation in content["animations"]:
                animations[animation["state"]] = Animation.sheet_animation_from_json(animation["anim"])

        return cls(parent, animations, content["defaultState"])