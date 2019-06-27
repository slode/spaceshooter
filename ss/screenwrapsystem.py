from triton.ecs import System

from .events import *
from .components import *

class ScreenwrapSystem(System):
    def initialize(self):
        self.on(TickEvent, self.update)

    def update(self, _):
        for e, (p, v) in self.registry.get_components(
                Position, Velocity):
            for e, (g,) in self.registry.get_components(
                    GameState):
                if g.screen_size == (0,0):
                    return

                if p.x < 0:
                    p.x = g.screen_size[0]
                elif p.x > g.screen_size[0]:
                    p.x = 0
                if p.y < 0:
                    p.y = g.screen_size[1]
                elif p.y > g.screen_size[1]:
                    p.y = 0
