from triton.ecs import System

from .events import *
from .components import *

from ss.sprites import SpriteLoader

class AnimationTickEvent(Event):
    pass

class AnimationEvent(Event):
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
    
    def __init__(self, entity, state=DEFAULT):
        self.entity = entity
        self.state = state

class AnimationStopEvent(Event):
    def __init__(self, entity):
        self.entity = entity

class SpriteSheet:
    def __init__(self, sprites):
        self.sprites = sprites

def sprite_by_slices(filename, slices):
    ss = SpriteLoader(filename)
    sprites = {}
    for k,v in slices.items():
        sprites[k] = ss.images_at(v, colorkey=-1)
    return SpriteSheet(sprites)

def generate_grid(slice_size=(10,10), grid_size=(1,1)):
    slices = []
    for r in range(grid_size[0]):
        for c in range(grid_size[1]):
            slices.append((r*slice_size[0], c*slice_size[1], slice_size[0], slice_size[1]))
    return slices

class AnimationSystem(System):
    def initialize(self):
        self.on(AnimationTickEvent, self.update_animation)
        #self.on(AnimationStopEvent, self.on_animation_stop)
        self.on(AnimationEvent, self.on_animation_event)
        self.on(TickEvent, self.on_update)

        self._spritesheets = {}
        self._last_update = 0.0

    def add_sprite(self, key, spritesheet):
        self._spritesheets[key] = spritesheet

    def update_animation(self, _):
        for e, (g,) in self.registry.get_components(
                GameState):
            t = g.t

        for e, (p, a, r) in self.registry.get_components(
                Position, Animatable, Renderable):

            if a.sprites is None:
                self.emit(AnimationEvent(e))
                continue
            
            if a.frame_index == len(a.sprites) - 1 and not a.loopable:
                self.emit(AnimationStopEvent(e))
                continue

            if  r.image is None or (t - a.frame_timer) > (1000 / a.frame_rate):
                a.frame_timer = t
                a.frame_index = (a.frame_index + 1) % len(a.sprites)
                r.image = a.sprites[a.frame_index]

            r.rect = r.image.get_rect()
            r.rect.center = (p.x, p.y)


    def on_animation_event(self, animation_event):
        try:
            a, = self.registry.get_entity(
                    animation_event.entity, Animatable)
        except KeyError:
            return

        if animation_event.state == a.animation_state:
            return

        a.animation_state = animation_event.state
        spritesheet = self._spritesheets[a.sprite_entity]

        try:
            a.sprites = spritesheet.sprites[a.animation_state]
        except:
            a.sprites = spritesheet.sprites[AnimationEvent.DEFAULT]

        a.frame_index = 0

    def on_animation_stop(self, stopev):
        [a] = self.registry.get_entity(
                startev.entity, Animatable)

        self.emit(AnimationEvent(stopev.entity))

    def on_update(self, _):
        for e, [a] in self.registry.get_components(Animatable):
            [up, down, left, right, shoot] = self.registry.get_entity(
                    e, UpAccel, DownAccel, LeftAccel, RightAccel, Shooting)

            if down and right:
                self.emit(AnimationEvent(e, AnimationEvent.BACKRIGHT))
            elif down and left:
                self.emit(AnimationEvent(e, AnimationEvent.BACKLEFT))
            elif down:
                self.emit(AnimationEvent(e, AnimationEvent.BACKCENTER))
            elif up and right:
                self.emit(AnimationEvent(e, AnimationEvent.UPRIGHT))
            elif up and left:
                self.emit(AnimationEvent(e, AnimationEvent.UPLEFT))
            elif up:
                self.emit(AnimationEvent(e, AnimationEvent.UPCENTER))
            elif right and not left:
                self.emit(AnimationEvent(e, AnimationEvent.RIGHT))
            elif not right and left:
                self.emit(AnimationEvent(e, AnimationEvent.LEFT))
            else:
                self.emit(AnimationEvent(e, AnimationEvent.DEFAULT))

            if shoot:
                self.emit(AnimationEvent(e, AnimationEvent.SHOOTING))

        for e, (g,) in self.registry.get_components(
                GameState):
            if g.t - self._last_update > 0: 
                self._last_update = g.t
                self.emit(AnimationTickEvent())
