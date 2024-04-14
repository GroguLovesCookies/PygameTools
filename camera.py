import pygame
from image import image_from_file
from classes.aabb import AABB
from vector.vector import Vector2


class Background:
    def __init__(self, img, parallax, stretch = (None, None)):
        self.img = image_from_file(img).convert_alpha()
        self.parallax = parallax

        if stretch[0] is not None:
            self.img = pygame.transform.scale(self.img, (stretch[0], self.img.get_rect().height))
        if stretch[1] is not None:
            self.img = pygame.transform.scale(self.img, (self.img.get_rect().width, stretch[1]))

    def draw(self, screen, size, scroll):
        width = self.img.get_rect().width
        num_to_draw = size.x//width + 2
        print(num_to_draw)
        for i in range(-(num_to_draw - 1), num_to_draw - 1):
            pos = scroll.x/self.parallax
            pos += (i - pos//width) * width
            screen.blit(self.img, (pos, size.y - self.img.get_rect().height))


class Camera:
    def __init__(self, scroll, bounds, screen_size, backgrounds):
        self.scroll = scroll
        self.bounds = bounds
        self.screen_size = screen_size
        self.backgrounds = backgrounds

    def draw_backgrounds(self, screen):
        for background in self.backgrounds:
            background.draw(screen, self.screen_size, self.scroll)

    def move_to(self, pos, smoothing):
        target = -pos + (self.screen_size * 0.5)
        self.scroll += (target - self.scroll)/smoothing
        if self.bounds is None:
            return

        if self.scroll.x < self.bounds.min.x:
            self.scroll.x = self.bounds.min.x
        elif self.scroll.x > self.bounds.max.x:
            self.scroll.x = self.bounds.max.x
        if self.scroll.y < self.bounds.min.y:
            self.scroll.y = self.bounds.min.y
        elif self.scroll.y > self.bounds.max.y:
            self.scroll.y = self.bounds.max.y
