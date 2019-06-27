from triton.ecs import System

from events import *
from components import *

class AnimationSystem(System):
    def initialize(self):
        self.on(AnimationTickEvent, self.update_animation)
        self.on(AccelEvent, self.on_accel)

    def on_accel(self, accel):
        [a, m] = self.registry.get_entity(
                accel.entity, Animatable, Movable)
        [s] = self.registry.get_entity(
                a.sprite_sheet, SpriteSheet)

        sprite_key = []
        if m.backward == 1:
            sprite_key.append("BW")
        else:
            sprite_key.append("FW")
        
        if m.left == m.right:
            sprite_key.append("CT")
        elif m.left == 1:
            sprite_key.append("LT")
        else:
            sprite_key.append("RG")

        key = "".join(sprite_key)
        if key in s.sprites:
            a.sprites = s.sprites[key]

    def update_animation(self, _):
        for e, (g,) in self.registry.get_components(
                GameState):
            t = g.t

        for e, (p, a) in self.registry.get_components(
                Position, Animatable):
            
            if a.sprites is None:
                [s] = self.registry.get_entity(
                        a.sprite_sheet, SpriteSheet)
                a.sprites = s.sprites["FWCT"]
            
            if  (t - a.previous_frame) > a.frame_rate:
                a.previous_frame = t
                a.frame_index = (a.frame_index + 1) % len(a.sprites)
                a.image = a.sprites[a.frame_index]
                a.rect = a.image.get_rect()
                a.rect.center = (p.x, p.y)

