from triton.ecs import System

from .events import *
from .components import *

class CollisionSystem(System):
    def initialize(self):
        self.on(TickEvent, self.check_for_collisions)

    def check_for_collisions(self, _):
        for e1, [r1, c1] in self.registry.get_components(Renderable, Collidable):
            if r1.rect is None:
                continue

            for e2, (r2, c2) in self.registry.get_components(Renderable, Collidable):

                if c1.team == c2.team:
                    continue

                if e2 <= e1:
                    continue

                if r2.rect is None:
                    continue

                if r1.rect.colliderect(r2.rect):
                    self.emit(CollisionEvent(e1, e2))

