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

    Instance = None
    
    def __init__(self, binds = DEFAULTS):
        self.binds = binds
        self.state = {"Axis": Vector2(0, 0)}
        self.pressed = []
        self.released = []
        InputHandler.Instance = self

    def update(self):
        self.pressed.clear()
        self.released.clear()
        self.state = {"Axis": Vector2(0, 0)}
        for key, category in self.DEFAULTS.items():
            key_states = pygame.key.get_pressed()
            if key_states[key.primary] or key_states[key.secondary]:
                self.state[category] += key.value
        
    def register_key_event(self, e):
        if e.type == pygame.KEYDOWN and e.key not in self.pressed:
            self.pressed.append(e.key)
        elif e.type == pygame.KEYUP and e.key not in self.released:
            self.released.append(e.key)

    def get_key_down(self, code):
        return code in self.pressed

    def get_key_up(self, code):
        return code in self.released
    
    def get_axis(self):
        return self.state["Axis"]

    def get_normalized_axis(self):
        return self.state["Axis"].normalized

    def get_axis_x(self):
        return self.state["Axis"].x