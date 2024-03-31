from typing import Tuple


"""
Converts cartesian coordinates to pygame coordinates
(0, 0) is the center of the screen
"""
def cartesian_to_pygame(x: int, y: int, screen_w: int, screen_h: int) -> Tuple[int, int]:
    x_pygame: int = screen_w//2 + x
    y_pygame: int = screen_h//2 - y

    return x_pygame, y_pygame


"""
Converts pygame coordinates to cartesian coordinates
"""
def pygame_to_cartesian(x: int, y: int, screen_w: int, screen_h: int) -> Tuple[int, int]:
    x_cart: int = x - screen_w//2
    y_cart: int = screen_h//2 - y
    
    return x_cart, y_cart



if __name__ == "__main__":
    print(cartesian_to_pygame(0, 300, 800, 600))
    print(pygame_to_cartesian(400, 0, 800, 600))
    