from triton.ecs import Component

class PlayerOne(Component):
    pass

class PlayerTwo(Component):
    pass

class Movable(Component):
    def __init__(self, forward=0, backward=0, left=0, right=0):
        self.forward = forward
        self.backward = backward
        self.left = left
        self.right = right

class Position(Component):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Velocity(Component):
    def __init__(self, x=0, y=0, attenuation=0.90):
        self.attenuation = attenuation
        self.x = x
        self.y = y

class Orientation(Component):
    def __init__(self, direction=1):
        self.direction = direction

class Weapon(Component):
    def __init__(self, damage=10, cooldown=3):
        self.damage = damage
        self.cooldown = cooldown
        self.countdown = 0

class AnimationStrip:
    def __init__(self):
        pass

class Animatable(Component):
    def __init__(self, sprite_sheet):
        self.sprite_sheet = sprite_sheet
        self.frame_rate = 30.0
        self.frame_index = 0
        self.previous_frame = 0
        self.image = None
        self.rect = None
        self.sprites = None

from sprites import spritesheet
class SpriteSheet(Component):
    def __init__(self, filename=None, **slices):
        ss = spritesheet(filename)
        self.sprites = {}
        for k,v in slices.items():
            self.sprites[k] = ss.images_at(v, colorkey=-1)

class Renderable(Component):
    pass

class Health(Component):
    def __init__(self, health=10):
        self.health = 10

class Collidable(Component):
    def __init__(self):
        self.rect = None

class GameState(Component):
    def __init__(self):
        self.running = True
        self.t = 0
        self.dt = 1.0
        self.screen_size = (0,0)
