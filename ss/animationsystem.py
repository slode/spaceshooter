from triton.ecs import System

from .events import *
from .components import *


class AnimationSystem(System):
    def initialize(self):
        self.on(AnimationTickEvent, self.update_animation)
        self.on(AnimationStopEvent, self.on_animation_stop)
        self.on(AnimationEvent, self.on_animation_event)
        self.on(TickEvent, self.on_update)

    def update_animation(self, _):
        for e, (g,) in self.registry.get_components(
                GameState):
            t = g.t

        for e, (p, a, r) in self.registry.get_components(
                Position, Animatable, Renderable):

            if a.sprites is None:
                self.emit(AnimationEvent(e))
                continue
            
            if  (t - a.frame_timer) > a.frame_rate:
                r.image = a.sprites[a.frame_index]
                a.frame_timer = t
                a.frame_index += 1
                r.rect = r.image.get_rect()
                r.rect.center = (p.x, p.y)

            if a.frame_index >= len(a.sprites):
                if not a.loopable:
                    self.emit(AnimationStopEvent(e))
                else:
                    a.frame_index = 0

    def on_animation_event(self, animev):
        [a] = self.registry.get_entity(
                animev.entity, Animatable)

        [sprite_comp] = self.registry.get_entity(
                a.sprite_entity,
                SpriteSheet)

        try:
            a.sprites = sprite_comp.sprites[animev.state]
        except:
            a.sprites = sprite_comp.sprites[AnimationEvent.DEFAULT]

        a.frame_index = 0

    def on_animation_stop(self, stopev):
        [a] = self.registry.get_entity(
                startev.entity, Animatable)
        if a.loopable:
            a.frame_index = 0
        else:
            self.emit(AnimationEvent(stopev.entity))

    def on_update(self, _):
        self.emit(AnimationTickEvent())
