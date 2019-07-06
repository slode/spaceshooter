from triton.ecs import System

from .events import *
from .components import *

class ProjectileSystem(System):
    def initialize(self):
        self.on(TickEvent, self.handle_cooldowns)
        self.on(ShootEvent, self.on_shootevent)

    def handle_cooldowns(self, event):
        for e, (g,) in self.registry.get_components(
                GameState):
            dt = g.dt

        for e, (p, w) in self.registry.get_components(
                Position, Weapon):
            if w.countdown > 0:
                w.countdown -= dt/1000

    def on_shootevent(self, event):
        (p, w) = self.registry.get_entity(
                event.entity,
                Position, Weapon)
        if w.countdown <= 0:
            w.countdown = w.cooldown
            rocket_sprite = self.registry.add_entity(
                    SpriteSheet(filename="res/rocket.bmp",
                                slices = {AnimationEvent.DEFAULT: [(0, 0, 15, 50), (0, 15, 15, 50)] }))
            self.registry.add_entity(
                    Position(x=p.x, y=p.y),
                    Velocity(),
                    Movable(forward=1),
                    Renderable(),
                    Collidable(),
                    Animatable(rocket_sprite))
            self.emit(AnimationEvent(event.entity, AnimationEvent.SHOOTING))
