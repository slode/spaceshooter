from triton.ecs import System

from .events import *
from .components import *

class AnimationStartEvent(Event):
    pass

class AnimationStopEvent(Event):
    pass

class AnimationSystem(System):
    def initialize(self):
        self.on(AnimationTickEvent, self.update_animation)
        self.on(AccelEvent, self.on_accel_event)
        self.on(AnimationStopEvent, self.on_animation_stop)
        self.on(AnimationStartEvent, self.on_animation_start)
#        self.on(EntityStateChangeEvent, self.on_state_change)

    def on_state_change(self, stateev):
        pass

    def on_accel_event(self, accelev):
        [a, m, s] = self.registry.get_entity(
                accel.entity, Animatable, MotionState)

        [s] = self.registry.get_entity(
                a.sprite_sheet, SpriteSheet)

        a.sprites = s.sprites[s]

    def update_animation(self, _):
        for e, (g,) in self.registry.get_components(
                GameState):
            t = g.t

        for e, (p, a) in self.registry.get_components(
                Position, Animatable):
            
            if a.sprites is None:
                [s] = self.registry.get_entity(
                        a.sprite_sheet, SpriteSheet)
                a.sprites = s.sprites[EntityState.DEFAULT]
            
            if  (t - a.previous_frame) > a.frame_rate:
                self.emit(AnimationStopEvent(e))
                a.previous_frame = t
                a.frame_index = (a.frame_index + 1) % len(a.sprites)
                a.image = a.sprites[a.frame_index]
                a.rect = a.image.get_rect()
                a.rect.center = (p.x, p.y)

    def on_animation_start(self, startev):
        pass

    def on_animation_stop(self, stopev):
        pass

