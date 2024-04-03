import pygame
from classes.custom_sprite import CustomSprite, Anchors
from vector.vector import Vector2
from components.rigid_body import RigidBodyComponent
from components.circle_collider import CircleCollider


SIZE = Vector2(800, 600)
FPS = 60

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE.toarray())
pygame.display.set_caption("Pygame Utils")
sprites = pygame.sprite.Group()
colliders = []

# platform = CustomSprite(Vector2(0, Anchors.SNAP_TO_BOTTOM), Vector2(Anchors.FILL_HORIZONTAL, 20), (100, 0, 0), SIZE, Anchors.CENTER_X|Anchors.BOTTOM_Y)
# sprites.add(platform)

player = CustomSprite(Vector2(0, 0), Vector2(40, 40), (0, 0, 100), SIZE, Anchors.CENTER_X|Anchors.CENTER_Y)
player.add_component(RigidBodyComponent, 2)
player.add_component(CircleCollider, colliders, 20)
sprites.add(player)

collidable = CustomSprite(Vector2(0, Anchors.SNAP_TO_BOTTOM), Vector2(40, 40), (0, 100, 0), SIZE, Anchors.CENTER_X|Anchors.BOTTOM_Y)
coll = collidable.add_component(CircleCollider, [], 20)
colliders.append(coll)
sprites.add(collidable)

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for sprite in sprites:
        sprite.tick()
        screen.blit(sprite.surface, sprite.rect)


    pygame.display.update()

    clock.tick(FPS)

pygame.quit()