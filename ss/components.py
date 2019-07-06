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
        self.state = self.DEFAULT

class Position(Component):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Velocity(Component):
    def __init__(self, x=0, y=0, attenuation=0.90):
        self.attenuation = attenuation
        self.x = x
        self.y = y

class Weapon(Component):
    def __init__(self, sprite_name=None, damage=10, cooldown=0.5):
        self.sprite_name = sprite_name
        self.damage = damage
        self.cooldown = cooldown
        self.countdown = 0

class Animatable(Component):
    def __init__(self, sprite_entity):
        self.sprite_entity = sprite_entity
        self.frame_rate = 30.0
        self.frame_index = 0
        self.frame_timer = 0
        self.loopable = True
        self.sprites = None

from ss.sprites import SpriteLoader
class SpriteSheet(Component):
    def __init__(self, filename=None, slices={}):
        ss = SpriteLoader(filename)
        self.sprites = {}
        for k,v in slices.items():
            self.sprites[k] = ss.images_at(v, colorkey=-1)

class Renderable(Component):
    def __init__(self):
        self.image = None
        self.rect = None

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
