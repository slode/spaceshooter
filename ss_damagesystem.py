from triton.ecs import System

from ss_events import *
from ss_components import *

class DamageSystem(System):
    def initialize(self):
        self.on(TickEvent, self.update)

    def update(self, _):
        pass
