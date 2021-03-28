from triton.ecs import System

from .events import *
from .components import *

class GameStateSystem(System):
    def initialize(self):
        self.on(TickEvent, self.update)
        self.on(GameExitEvent, self.exit)
        self.emit(TickEvent())
        self._last_second = 0.0

    def exit(self, _):
        for e, (g,) in self.registry.get_components(
                GameState):
            g.running = False
            if g.t - self._last_second > 1000:
                self._last_second = g.t
                self.emit(SecondTickEvent())
            

    def update(self, _):
        self.emit(TickEvent())
