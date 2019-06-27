from triton.ecs import System

from ss_events import *
from ss_components import *

class CollisionSystem(System):
    def initialize(self):
        self.on(TickEvent, self.check_for_collisions)
        pass

    def check_for_collisions(self, _):
        pass

