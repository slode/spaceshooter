from triton.ecs import Component

class PlayerOne(Component):
    pass

class PlayerTwo(Component):
    pass

class Movable(Component):
    def __init__(self):
        self.forward = 0
        self.backward = 0
        self.left = 0
        self.right = 0

class EntityState(Component):
    UPLEFT=1
    UPCENTER=2
    UPRIGHT=3
    LEFT=4
    DEFAULT=5
    RIGHT=6
    BACKLEFT=7
    BACKCENTER=8
    BACKRIGHT=9
    SHOOTING=10
    EXPLODING=11

    def __init__(self):
        self.direction = self.DEFAULT

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

class Animatable(Component):
    def __init__(self, sprite_sheet):
        self.sprite_sheet = sprite_sheet
        self.frame_rate = 30.0
        self.frame_index = 0
        self.previous_frame = 0
        self.image = None
        self.rect = None
        self.sprites = None

from ss.sprites import SpriteLoader
class SpriteSheet(Component):
    def __init__(self, filename=None, **slices):
        ss = SpriteLoader(filename)
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
