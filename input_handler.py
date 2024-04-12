import pygame
from vector.vector import Vector2


class KeyBind:
    def __init__(self, name, primary, secondary=None, gradual=False, value = 1):
        self.primary = primary
        self.secondary = secondary
        self.gradual = gradual
        self.name = name
        self.value = value


class InputHandler:
    LEFT = KeyBind("Left", pygame.K_a, pygame.K_LEFT, True, Vector2(-1, 0))
    RIGHT = KeyBind("Right", pygame.K_d, pygame.K_RIGHT, True, Vector2(1, 0))
    UP = KeyBind("Up", pygame.K_w, pygame.K_UP, True, Vector2(0, 1))
    DOWN = KeyBind("Down", pygame.K_s, pygame.K_DOWN, True, Vector2(0, -1))

    DEFAULTS = {
        LEFT: "Axis",
        RIGHT: "Axis",
        UP: "Axis",
        DOWN: "Axis"
    }
    
    def __init__(self, binds = DEFAULTS):
        self.binds = binds
        self.state = {"Axis": Vector2(0, 0)}

    def update(self):
        self.state = {"Axis": Vector2(0, 0)}
        for key, category in self.DEFAULTS.items():
            key_states = pygame.key.get_pressed()
            if key_states[key.primary] or key_states[key.secondary]:
                self.state[category] += key.value
    
    def get_axis(self):
        return self.state["Axis"]

    def get_normalized_axis(self):
        return self.state["Axis"].normalized