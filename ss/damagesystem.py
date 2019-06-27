from triton.ecs import System

from events import *
from components import *

class DamageSystem(System):
    def initialize(self):
        self.on(TickEvent, self.update)

    def update(self, _):
        pass
