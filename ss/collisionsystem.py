from triton.ecs import System

from .events import *
from .components import *

class CollisionSystem(System):
    def initialize(self):
        self.on(TickEvent, self.check_for_collisions)
        pass

    def check_for_collisions(self, _):
        pass

