# PygameTools
This is a collection of tools for pygame to streamline development of games by reducing time spent on tasks such as physics, camera controls, tilemaps, etc.

# Features
## CustomSprite
A more advanced sprite class. Can be an image, polygon or circle.
```python
a = CustomSprite(position, radius, color, screen_size, anchor, CustomSprite.TYPE_CIRCLE) # Creates a circular sprite at position with set radius
b = CustomSprite(position, vertices, color, screen_size, anchor, CustomSprite.TYPE_POLYGON, rotation) # Creates a polygon with set vertices, position and rotation
c = CustomSprite.create_rectangular_sprite(position, size, color, screen_size, rotation, anchor) # Creates a rectangle centered at position with set size and rotation
d = CustomSprite.create_image_sprite(position, "images/sample.png", screen_size, rotation, anchor) # Creates a sprite whose texture is "images/sample.png" with a certain rotation
```
