from triton.ecs import System

from .events import *
from .components import *

class AnimationStartEvent(Event):
    def __init__(self, entity):
        self.entity = entity

class AnimationStopEvent(Event):
    def __init__(self, entity):
        self.entity = entity

class AnimationSystem(System):
    def initialize(self):
        self.on(AnimationTickEvent, self.update_animation)
        self.on(AnimationStopEvent, self.on_animation_stop)
        self.on(AnimationStartEvent, self.on_animation_start)
        self.on(EntityStateEvent, self.on_state_change)

    def on_state_change(self, stateev):
        [a, s] = self.registry.get_entity(
                stateev.entity, Animatable, EntityState)

        [sprite_comp] = self.registry.get_entity(
                a.sprite_entity,
                SpriteSheet)

        a.sprites = sprite_comp.sprites[s.state]

    def update_animation(self, _):
        for e, (g,) in self.registry.get_components(
                GameState):
            t = g.t

        for e, (p, a, r) in self.registry.get_components(
                Position, Animatable, Renderable):

            if a.sprites is None:
                self.emit(AnimationStartEvent(e))
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

    def on_animation_start(self, startev):
        [a, s] = self.registry.get_entity(
                startev.entity, Animatable, EntityState)

        [sprite_comp] = self.registry.get_entity(
                a.sprite_entity,
                SpriteSheet)

        a.sprites = sprite_comp.sprites[s.state]

    def on_animation_stop(self, stopev):
        [a] = self.registry.get_entity(
                startev.entity, Animatable)
        if a.loopable:
            a.frame_index = 0
        else:
            self.emit(AnimationStartEvent(stopev.entity))
