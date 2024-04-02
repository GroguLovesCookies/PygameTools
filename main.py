import pygame
from classes.custom_sprite import CustomSprite, Anchors
from vector.vector import Vector2
from components.rigid_body import RigidBodyComponent


SIZE = Vector2(800, 600)
FPS = 60

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE.toarray())
pygame.display.set_caption("Pygame Utils")
sprites = pygame.sprite.Group()

platform = CustomSprite(Vector2(0, Anchors.SNAP_TO_BOTTOM), Vector2(Anchors.FILL_HORIZONTAL, 20), (100, 0, 0), SIZE, Anchors.CENTER_X|Anchors.BOTTOM_Y)
sprites.add(platform)

player = CustomSprite(Vector2(Anchors.SNAP_TO_RIGHT, 0), Vector2(40, 40), (0, 0, 100), SIZE, Anchors.RIGHT_X|Anchors.CENTER_Y)
player.add_component(RigidBodyComponent, 2)
sprites.add(player)

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for sprite in sprites:
        sprite.tick()
        screen.blit(sprite.surface, sprite.rect)

    print(player.pos)

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()