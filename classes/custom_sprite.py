import pygame


class CustomSprite(pygame.sprite.Sprite):
    def __init__(self, rect, col):
        super().__init__()
        self.surface = pygame.Surface((rect[2], rect[3]))
        self.surface.fill(col)
        self.rect = self.surface.get_rect()
        self.rect.left = rect[0]
        self.rect.top = rect[1]
