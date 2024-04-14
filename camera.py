import pygame
from image import image_from_file
from classes.aabb import AABB
from vector.vector import Vector2


class Background:
    def __init__(self, images, parallax, stretch = (None, None), repeat = (True, False)):
        self.images = []
        self.parallax = parallax

        for image_path in images:
            img = image_from_file(image_path).convert_alpha()
            if stretch[0] is not None:
                img = pygame.transform.scale(img, (stretch[0], img.get_rect().height))
            if stretch[1] is not None:
                img = pygame.transform.scale(img, (img.get_rect().width, stretch[1]))
            self.images.append(img)

        self.repeat = repeat

    def draw(self, screen, size, scroll):
        if self.repeat[0]:
            width = self.images[0].get_rect().width
            num_to_draw = size.x//width + 2
            for i in range(-(num_to_draw - 1), num_to_draw - 1):
                pos = scroll.x/self.parallax
                true_pos = (i - pos//width) * width + pos
                self.draw_strip(true_pos, screen, size, scroll, int(i - pos//width + num_to_draw) % len(self.images))
        else:
            self.draw_strip(0, screen, size, scroll)
            
    
    def draw_strip(self, pos_x, screen, size, scroll, sprite_to_use=0):
        img = self.images[sprite_to_use]
        if not self.repeat[1]:
            screen.blit(img, (pos_x, size.y - img.get_rect().height))
            return

        height = img.get_rect().height
        num_to_draw = size.x//height + 1
        for i in range(num_to_draw):
            pos_y = i * height
            screen.blit(img, (pos_x, pos_y))


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
