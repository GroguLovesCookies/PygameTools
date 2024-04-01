import pygame
from classes.custom_sprite import CustomSprite, Anchors


SIZE = (800, 600)
FPS = 60

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pygame Utils")
sprites = pygame.sprite.Group()


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        screen.fill((0, 0, 0))
        
        platform = CustomSprite((0, Anchors.SNAP_TO_BOTTOM, Anchors.FILL_HORIZONTAL, 20), (100, 0, 0), SIZE, Anchors.CENTER_X|Anchors.BOTTOM_Y)
        sprites.add(platform)

        player = CustomSprite((Anchors.SNAP_TO_RIGHT, 0, 40, 40), (0, 0, 100), SIZE, Anchors.RIGHT_X|Anchors.CENTER_Y)
        sprites.add(player)

        for sprite in sprites:
            screen.blit(sprite.surface, sprite.rect)

        pygame.display.update()

pygame.quit()