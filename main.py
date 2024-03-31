import pygame
from classes.custom_sprite import CustomSprite


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
        
        platform = CustomSprite((0, SIZE[1]-20, SIZE[0], 20), (100, 0, 0))
        sprites.add(platform)

        player = CustomSprite((SIZE[0]//2-20, SIZE[1]//2-20, 40, 40), (0, 0, 100))
        sprites.add(player)

        for sprite in sprites:
            screen.blit(sprite.surface, sprite.rect)

        pygame.display.update()

pygame.quit()