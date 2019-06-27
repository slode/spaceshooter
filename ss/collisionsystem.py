from triton.ecs import System

from .events import *
from .components import *

class CollisionSystem(System):
    def initialize(self):
        self.on(TickEvent, self.check_for_collisions)
        pass

    def check_for_collisions(self, _):
        for e1, (p1, v1, c1) in self.registry.get_components(
                Position, Velocity, Collidable):
            for e2, (p2, v2, c2) in self.registry.get_components(
                    Position, Velocity, Collidable):
                if e2 >= e1:
                    continue

