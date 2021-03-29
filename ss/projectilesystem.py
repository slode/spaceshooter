from triton.ecs import System

from .events import *
from .components import *

class ProjectileSystem(System):
    def initialize(self):
        self.on(TickEvent, self.handle_cooldowns)
        self.on(TickEvent, self.on_shootevent)

    def handle_cooldowns(self, event):
        for e, (g,) in self.registry.get_components(
                GameState):
            dt = g.dt

        for e, (p, w) in self.registry.get_components(
                Position, Weapon):
            if w.countdown > 0:
                w.countdown -= dt/1000

    def on_shootevent(self, event):
        for e, [s, p, w, c] in self.registry.get_components(Shooting, Position, Weapon, Collidable):

            if w.countdown <= 0:
                w.countdown = w.cooldown
                self.registry.add_entity(
                        Position(x=p.x, y=p.y),
                        Velocity(),
                        Health(),
                        UpAccel(),
                        Renderable(),
                        Collidable(team=c.team),
                        Animatable("rocket"))
