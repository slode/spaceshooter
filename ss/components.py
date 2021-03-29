from triton.ecs import Component

class LeftAccel(Component):
    pass

class RightAccel(Component):
    pass

class UpAccel(Component):
    pass

class DownAccel(Component):
    pass

class Shooting(Component):
    pass

class Player(Component):
    def __init__(self, keymap={}):
        self.key_map = keymap

class EntityAi(Component):
    def __init__(self):
        self.target = None
        self.close_range = False

class Position(Component):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Velocity(Component):
    def __init__(self, x=0, y=0, attenuation=0.90, max_speed=5.0):
        self.attenuation = attenuation
        self.x = x
        self.y = y
        self.max_speed = max_speed

class Accel(Component):
    def __init__(self, x=0, y=0, mass=100.0):
        self.x = x
        self.y = y
        self.mass = mass

class Weapon(Component):
    def __init__(self, sprite_name=None, damage=10, cooldown=0.5):
        self.sprite_name = sprite_name
        self.damage = damage
        self.cooldown = cooldown
        self.countdown = 0

class Animatable(Component):
    def __init__(self, sprite_entity, loopable=True, frame_rate=30):
        self.sprite_entity = sprite_entity
        self.frame_rate = frame_rate
        self.frame_index = 0
        self.frame_timer = 0
        self.loopable = loopable
        self.sprites = None
        self.animation_state = None

class Renderable(Component):
    def __init__(self):
        self.image = None
        self.rect = None

class Health(Component):
    def __init__(self, health=10):
        self.health = health
        self.die_duration = 1.0

class Collidable(Component):
    def __init__(self, team=1):
        self.team = team
        self.rect = None

class GameState(Component):
    def __init__(self):
        self.running = True
        self.t = 0
        self.dt = 1.0
        self.screen_size = (0,0)
