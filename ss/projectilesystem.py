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
            dt = g.dt/1000

        for e, (p, w) in self.registry.get_components(
                Position, Weapon):
            if w.countdown > 0:
                w.countdown -= dt

    def on_shootevent(self, event):
        (p, w) = self.registry.get_entity(
                event.entity,
                Position, Weapon)
        if w.countdown <= 0:
            w.countdown = w.cooldown
            self.registry.add_entity(
                    Position(x=p.x, y=p.y),
                    Velocity(y=-1),
                    Movable(forward=1),
                    Renderable(),
                    Collidable())
