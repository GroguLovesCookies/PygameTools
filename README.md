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

## Components
Allow the adding of functionality to your sprites. To create a custom component, one must override the `Component` class with the following template:
```python
class CustomComponent(Component):
  COMPONENT_INDEX = 0 # Components are processed in order of their component index: i.e. a lower component index gets processed before a higher one.

  def __init__(self, parent, foo, bar, ...):
    "Parent argument is required, all others are component-specific"
    super().__init__(parent)
    ...

  def tick(self, time):
    "The behaviour of this component every frame"
    ...

  def late_tick(self, time):
    "The behaviour of this component after all components have received a tick() call"
    ...
```

To add a component to a sprite, call:
```python
my_custom_component = sprite.add_component(CustomComponent, foo, bar, ...) # Do not pass in parent, only component-specific arguments
```


